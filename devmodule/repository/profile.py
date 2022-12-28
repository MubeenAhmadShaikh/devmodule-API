from fastapi import FastAPI, Depends, status, HTTPException, Form, UploadFile, File
from sqlalchemy.orm import Session
from devmodule.repository.oauth2 import get_current_user
from devmodule.core import schemas, database, models
from sqlalchemy import event
import os
import re
from devmodule.drive import driveDB

# Get all the developers profiles
def view_all_profiles(db):
    '''
    This function is implemented to get all the profiles in db that exist.
    '''
    all_profiles = db.query(models.Profile).all()
    active_profiles = all_active_profiles(all_profiles)   
    return active_profiles

# To get the all active users only
def all_active_profiles(all_profiles):
    active_profiles = []
    for profile in all_profiles:
        if profile.is_active:
            active_profiles.append(profile)
         
    return active_profiles

# Search the users for profiles
def search_profiles(query:str, db:Session =Depends(database.get_db)):
    all_profiles = db.query(models.Profile).filter(
        models.Profile.first_name.contains(query) |
        models.Profile.last_name.contains(query) |
        models.Profile.short_intro.contains(query) 
     ).all()
    
    if all_profiles:
        return all_active_profiles(all_profiles)
    else:
        skill_filter = db.query(models.Skill).filter(
        models.Skill.name.contains(query)).all()
        for skill in skill_filter:
            all_profiles.append(skill.owner)
        all_profiles = all_active_profiles(all_profiles)
    return all_profiles

# To get the single profile using the id parameter
def view_single_profile(id:int, db:Session =Depends(database.get_db)):
    user_profile = db.query(models.Profile).filter(models.Profile.id == id).first()
    if not user_profile:
              raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No such profile exist')
    return user_profile

#To create basic info of profile 
def create_profile(username,first_name,last_name, db:Session =Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == username).first()
    create_profile = models.Profile(
        first_name = first_name,
        last_name = last_name,
        username = username,
        is_active=True,
        user_id= user.id
    )
    db.add(create_profile)
    db.commit()
    db.refresh(create_profile)
    return True

#Update profile for user
def update_profile(
    first_name,
    last_name,
    profile_image,
    location,
    short_intro,
    bio,
    social_github,
    social_twitter,
    social_linkedin,
    social_youtube,
    social_website, 
    db:Session =Depends(database.get_db), 
    current_user: models.User = Depends(get_current_user)):
    user_profile = db.query(models.Profile).filter(models.Profile.id == current_user.id)
    try:    
        # user = db.query(models.User).filter(models.User.id == user_profile.first().user_id)
        if not user_profile.first():
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='No such profile exist')
        f = open(os.path.realpath(os.curdir)+'/temp/profile_images/'+profile_image.filename, 'wb')
        f.write(profile_image.file.read())
        f.close()
        page = 'profile'
        profile_img_id = driveDB.upload_file(profile_image.filename,os.path.realpath(os.curdir)+'/temp/profile_images/'+profile_image.filename, page)
        weburl = driveDB.get_file_with_id(profile_img_id).get('webContentLink')
        profileObj = db.query(models.Profile).filter(models.Profile.id == current_user.id).first()
        if profileObj.profile_image:
            prev_image_id = re.search('=(.*?)&', profileObj.profile_image).group(1)
            delete_image(prev_image_id)
        user_profile.update({
            'first_name':first_name,
            'last_name':last_name,
            'profile_image':weburl,
            'location':location,
            'short_intro':short_intro,
            'bio':bio,
            'social_github':social_github,
            'social_twitter':social_twitter,
            'social_linkedin':social_linkedin,
            'social_youtube':social_youtube,
            'social_website':social_website,
        })
        db.commit()
        os.remove(os.path.realpath(os.curdir) + '/temp/profile_images/' + profile_image.filename)
        response = "Profile updated"
        return response
    except:
        response = "Something went wrong"
        return response

# Specific function to delete the image
def delete_image(id:str):
    return driveDB.delete_file(id)

# To Deactivate the user profile
def deactivate_user(db:Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    is_active1 = {
        'is_active': False
    }
    user_profile = db.query(models.Profile).filter(models.Profile.user_id ==  current_user.id)
    if not user_profile.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No such user exist')
    user_profile.update(is_active1)
    db.commit()
    return 'User Deleted'