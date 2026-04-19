from .. import models,schemas,utils
from fastapi import HTTPException,Depends,FastAPI,APIRouter
from sqlalchemy.orm import Session
from ..database import get_db

router=APIRouter(
    prefix="/users",
    tags=['USERS']
)

@router.post("/",response_model=schemas.UserResponse)
def create_user(new_user:schemas.UserCreate,db:Session=Depends(get_db)):
    #hashing the password
    hashed_password=utils.hash(new_user.password)
    new_user.password=hashed_password


    user_dict=new_user.model_dump()
    new_user=models.User(**user_dict)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.get("/{id}",response_model=schemas.UserResponse)
def get_users(id:int,db:Session=Depends(get_db)):

    user=db.query(models.User).filter(models.User.id==id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return user


   
    

    