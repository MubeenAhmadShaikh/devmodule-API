from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from devmodule.core import models, database, schemas


#TODO
# 1. write the lambda functions for storing the major and moinor skills 
# in both SINGLE_SKILL and ALL_SKILL function


# To create a skill
def create_skill(request, db,current_user):
    for skill in current_user.skill:
        if (skill.name == request.name.lower()):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Already have this skill in your profile')
    create_skill = models.Skill(
        name=request.name.lower(),
        description=request.description,
        owner_id=current_user.id
    )
    db.add(create_skill)
    db.commit()
    db.refresh(create_skill)
    return create_skill

# To update a skill
def update_skill(id:int, request:schemas.skillBase,db:Session = Depends(database.get_db)):
    update_skill = db.query(models.Skill).filter(models.Skill.id == id)
    if not update_skill.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No such skill exist')
    update_skill.update(request.dict())
    db.commit()
    return 'Updated skill'

# To delete a skill
def delete_skill(id:int, db:Session = Depends(database.get_db)):
    delete_skill = db.query(models.Skill).filter(models.Skill.id == id)
    if not delete_skill.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No such skill exist')
    delete_skill.delete()
    db.commit()
    return 'Deleted skill'


# To get single skill
def view_single_skill(id:int, db:Session = Depends(database.get_db)):
    single_skill = db.query(models.Skill).filter(models.Skill.id == id).first()
    if not single_skill:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No such skill exist')
    return single_skill

# To view all skill
def view_all_skills(db:Session = Depends(database.get_db)):
    all_skills = db.query(models.Skill).all()
    return all_skills
    