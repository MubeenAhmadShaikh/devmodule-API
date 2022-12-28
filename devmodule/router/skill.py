from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from devmodule.core import models, database, schemas
from devmodule.repository import skill
from devmodule.repository.oauth2 import get_current_user

router = APIRouter(
    prefix='/skills',
    tags=['Skill']
)


# route for creating a skill
@router.post('/create-skill', status_code=status.HTTP_201_CREATED)
def create_skill(request:schemas.skillBase, db:Session = Depends(database.get_db),current_user: schemas.UserBase = Depends(get_current_user)):
    return skill.create_skill(request, db,current_user)

# route for updating a skill
@router.put('/update-skill/{id}', status_code=status.HTTP_200_OK)
def update_skill(id:int,request:schemas.skillBase, db:Session = Depends(database.get_db)):
    return skill.update_skill(id, request, db)

# route for deleting a skill
@router.delete('/delete-skill/{id}', status_code=status.HTTP_200_OK)
def delete_skill(id:int, db:Session = Depends(database.get_db)):
    return skill.delete_skill(id, db)

# route for viewing single skill
@router.get('/single-skill/{id}')
def view_single_skill(id:int, db:Session = Depends(database.get_db)):
    return skill.view_single_skill(id,db)

# route for viewing all skill
@router.get('/all-skills')
def view_all_skills(db:Session = Depends(database.get_db)):
    return skill.view_all_skills(db)


