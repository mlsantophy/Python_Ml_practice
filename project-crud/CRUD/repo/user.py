from typing import List
from sqlalchemy.orm import Session
from .. import models,schemas,database
from fastapi import HTTPException,status, APIRouter,Depends
from .. hashing import Hash

router=APIRouter(tags=['users'])

get_db=database.get_db

def create(request:schemas.User,db:Session):
    new_user=models.User(name=request.name,email=request.email,password=Hash.bcrypt(request.password),hm_adrs=request.hm_adrs,offi_adrs=request.offi_adrs)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_all(db:Session):
    users=db.query(models.User).all()
    return users

def show(id:int,db:Session):
    all_user=db.query(models.User).filter(models.User.id==id).first()
    if not all_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                             detail=f'user with id {id} not found')
    return all_user

def update(id:int,request:schemas.User,db:Session):
    users=db.query(models.User).filter(models.User.id==id)
    if not users.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                             detail=f'User with id {id} not found')
    users.update(request.dict())
    
    db.commit()
    db.refresh
    return 'updated'

def destroy(id:int,db:Session):
    users=db.query(models.User).filter(models.User.id==id)
    if not users.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with id {id} not available")
    users.delete(synchronize_session=False)
    db.commit()
    return 'deleted successfully'
