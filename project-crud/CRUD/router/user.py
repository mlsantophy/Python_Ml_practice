from typing import List
from fastapi import APIRouter, Depends,status,HTTPException,Response
from .. import schemas, database,models,oauth2
from sqlalchemy.orm import Session
from ..repo import user

router=APIRouter(tags=['user'])

get_db=database.get_db

@router.post('/user')
def create_user(request:schemas.User,db:Session=Depends(get_db),current_user:schemas.User=Depends(oauth2.get_current_user)): 
    return user.create(request,db)

@router.get('/user',response_model=List[schemas.ShowUser])
def get_all(db:Session=Depends(get_db),
            current_user:schemas.User=Depends(oauth2.get_current_user)):
    return user.get_all(db)

@router.get('/user/{id}')
def show(id:int,response:Response,db:Session=Depends(get_db),
         current_user:schemas.User=Depends(oauth2.get_current_user)):
    return user.show(id,db)

 
@router.put('/user/{id}')            
def update(id:int,request:schemas.User,db:Session=Depends(get_db),
           current_user:schemas.User=Depends(oauth2.get_current_user)):
    return user.update(id,request,db)

@router.delete('/user/{id}')
def destroy (id:int,db:Session=Depends(get_db),
             current_user:schemas.User=Depends(oauth2.get_current_user)):
    return user.destroy(id,db)