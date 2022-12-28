
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, File, UploadFile
from devmodule.core import schemas, database, models
from devmodule.repository.oauth2 import get_current_user
from devmodule.repository import project, profile
import shutil
import os
import re
from pathlib import Path
from devmodule.drive import driveDB

# To get all the projects
def view_all_projects(db:Session = Depends(database.get_db)):
    projects = db.query(models.Project).all()
    profiles= [project.owner for project in projects]
    active_profiles = profile.all_active_profiles(profiles)
    active_projects=all_active_profiles_projects(projects)
    return active_projects, active_profiles

# To get single project with id
def view_single_project(id:int, db:Session = Depends(database.get_db)):
    single_project = db.query(models.Project).filter(models.Project.id == id).first()
    
    if not single_project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No such Project exist")
    return single_project



# To create a project
def create_project(title,featured_image,description,demo_link,source_link, db:Session= Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    try :
        f = open(os.path.realpath(os.curdir)+'/temp/project_images/'+featured_image.filename, 'wb')
        f.write(featured_image.file.read())
        f.close()
        page = 'project'
        feature_img_id = driveDB.upload_file(featured_image.filename,os.path.realpath(os.curdir)+'/temp/project_images/'+featured_image.filename, page)
        weburl = driveDB.get_file_with_id(feature_img_id).get('webContentLink')
        print(weburl)
        create_project = models.Project(
            title=title,
            featured_image=weburl,
            description=description,
            demo_link=demo_link,
            source_link=source_link,
            vote_total=0,
            vote_ratio=0,
            owner_id=current_user.id
            )
        db.add(create_project)
        db.commit()
        db.refresh(create_project)      
        os.remove(os.path.realpath(os.curdir) + '/temp/project_images/' + featured_image.filename)
        return create_project
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unable to Create project")

    

# To update a project
def update_project(id:int,title,featured_image,description,demo_link,source_link, db:Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    single_project = db.query(models.Project).filter(models.Project.id == id)
    if not single_project.first():
              raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='No such project exist')
    try:
        f = open(os.path.realpath(os.curdir)+'/temp/project_images/'+featured_image.filename, 'wb')
        f.write(featured_image.file.read())
        f.close()
        page = 'project'
        feature_img_id = driveDB.upload_file(featured_image.filename,os.path.realpath(os.curdir)+'/temp/project_images/'+featured_image.filename, page)
        weburl = driveDB.get_file_with_id(feature_img_id).get('webContentLink')
        projectObj = db.query(models.Project).filter(models.Project.id == id).first()
        prev_image_id = re.search('=(.*?)&', projectObj.featured_image).group(1)
        delete_image(prev_image_id)
        single_project.update({
            'title':title,
            'featured_image':weburl,
            'description':description,
            'demo_link':demo_link,
            'source_link':source_link,
        })
        db.commit()
        os.remove(os.path.realpath(os.curdir) + '/temp/project_images/' + featured_image.filename)
        return 'Project updated'
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unable to Update project")
   
# To delete an image from drivedb
def delete_image(id:str):
    return driveDB.delete_file(id)


# To Delete single project
def delete_project(id:int,db:Session = Depends(database.get_db)):
    single_project = db.query(models.Project).filter(models.Project.id == id)
    projectObj = db.query(models.Project).filter(models.Project.id == id).first()
    prev_image_id = re.search('=(.*?)&', projectObj.featured_image).group(1)
    delete_image(prev_image_id)
    if not single_project.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No such project exist")
    single_project.delete()
    db.commit()
    return 'Project Deleted'

# To get all the reviews of a project
def get_project_review(id,db):
    projectObj = project.view_single_project(id,db)
    reviews = projectObj.review
    return all_active_profiles_reviews(reviews)

# To search for the projects
def search_projects(query,db):
    all_projects = db.query(models.Project).filter(
    models.Project.title.contains(query) |
    models.Project.description.contains(query) 
    ).all()

    if all_projects:
        return all_active_profiles_projects(all_projects)
    else:
        projects = db.query(models.Project).all()
        active_projects = all_active_profiles_projects(projects)
        all_projects = []
        for project in active_projects:
            if (project.owner.first_name.lower() in query.lower()) or (project.owner.last_name.lower() in query.lower()) :
                all_projects.append(project)
            print(len(all_projects))
        return all_projects
            
# To return only active profiles projects
def all_active_profiles_projects(all_projects):
    active_projects=[]
    for project in all_projects:
        if (project.owner.is_active):
            active_projects.append(project)
    return active_projects

# To return only active profiles reviews
def all_active_profiles_reviews(all_reviews):
    active_reviews=[]
    for review in all_reviews:
        if (review.owner.is_active):
            active_reviews.append(review)
    return active_reviews