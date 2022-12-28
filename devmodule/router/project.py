
from fastapi import FastAPI, Depends, Request, status, APIRouter, UploadFile, File, Form
from sqlalchemy.orm import Session
from devmodule.repository import project
from devmodule.repository.oauth2 import get_current_user
from devmodule.core import schemas, database, models
from typing import  Union
router = APIRouter(
    prefix='/projects',
    tags=['Projects']
)

# Route for creating a project
@router.post('/create-project', status_code=status.HTTP_201_CREATED)
def create_project(
    title:str = Form(...),
    featured_image:UploadFile = File(...),
    description:str = Form(...),
    demo_link:str = Form(...),
    source_link:str = Form(...),
    db:Session= Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    return project.create_project(title,featured_image, description,demo_link,source_link, db, current_user)

# Route for updating a project
@router.put('/update-project/{id}', status_code=status.HTTP_200_OK)
def update_project(id:int,
    title:str = Form(...),
    featured_image:UploadFile = File(...),
    description:str = Form(...),
    demo_link:str = Form(...),
    source_link:str = Form(...),
    db:Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)):
    return project.update_project(id,title,featured_image,description,demo_link,source_link,db)

# Route for deleting a project
@router.delete('/delete-project/{id}')
def delete_project(id:int,db:Session = Depends(database.get_db),current_user: schemas.UserBase= Depends(get_current_user)):
    return project.delete_project(id,db)


# Route for viewing all project for authorized user
@router.get('/',status_code=status.HTTP_200_OK)
def view_all_projects(query: Union[str, None] = None, db:Session = Depends(database.get_db),current_user: schemas.UserBase= Depends(get_current_user)):    
    if(query):
        projects = project.search_projects(query,db)
        return {"projects":projects}
    else: 
        projects, profiles = project.view_all_projects(db)
        return {"projects":projects }
    

# Route for all projects for unauthorized user
@router.get('/projects-explore',status_code=status.HTTP_200_OK)
def view_all_projects( query: Union[str, None] = None, db:Session = Depends(database.get_db)):    
    if(query):
        projects = project.search_projects(query,db)
        return {"projects":projects}
    else: 
        projects, profiles = project.view_all_projects(db)
        return {"projects":projects,"profiles":profiles}

# Route for viewing single project for authorized user
@router.get('/project/{id}',status_code=status.HTTP_200_OK)
def view_single_project(id:int,db:Session = Depends(database.get_db),current_user: schemas.UserBase = Depends(get_current_user)):
    projectObject = project.view_single_project(id,db)
    owner = projectObject.owner
    reviews = project.get_project_review(id,db)
    return {"project":projectObject}


# Route for single projects for unauthorized user
@router.get('/project-explore/{id}',status_code=status.HTTP_200_OK)
def view_single_project(id:int,db:Session = Depends(database.get_db)): 
    projectObject = project.view_single_project(id,db)
    owner = projectObject.owner
    reviews = project.get_project_review(id, db)
    return {"project":projectObject}

# route for getting the review of a particular project
@router.get('/get-project-review/{prj_id}',status_code=status.HTTP_200_OK)
def get_project_review(id:int,db:Session= Depends(database.get_db), current_user = Depends(get_current_user)):
   return project.get_project_review(id,db)

