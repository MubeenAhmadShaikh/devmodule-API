
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from devmodule.repository import token
from devmodule.repository.hashing import Hash
from devmodule.core import models, database
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def get_current_user(tokendata: str = Depends(oauth2_scheme), db:Session = Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )       
    return token.verify_token(tokendata, credentials_exception, db)



def authenticate_user(request, db:Session = Depends(database.get_db)):
    
    user = db.query(models.User).filter(models.User.email == request.username )
    if (not user.first()) or (not Hash.verify_password(request.password, user.first().password)) :
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username",)
    activate_user={
        'is_active' : True
    }
    if not user.first().is_active:
        user.update(activate_user)
        db.commit()
    return user.first()
