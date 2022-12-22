from fastapi import FastAPI,Response,status,HTTPException
from fastapi import Depends,File,UploadFile
from . import schemas, models
from . database import engine,SessionLocal
from sqlalchemy.orm import Session
from .hashing import Hash
from .router import user,file,authentication

app=FastAPI()

models.Base.metadata.create_all(engine)


app.include_router(authentication.router)
app.include_router(user.router)
app.include_router(file.router)


# def get_db():
#     db=SessionLocal()
    
#     try:
#         yield db
#     finally:
#         db.close()
 
# @app.post('/user')

# def create_user(request:schemas.User,db:Session=Depends(get_db)):
#     new_user=models.User(name=request.name,email=request.email,password=Hash.bcrypt(request.password),hm_adrs=request.hm_adrs,offi_adrs=request.offi_adrs)
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     return new_user

# @app.get('/user')
# def get_all(db:Session=Depends(get_db)):
#     users=db.query(models.User).all()
#     return users

# @app.get('/user/{id}')
# def show(id:int,response:Response,db:Session=Depends(get_db)):
#     all_user=db.query(models.User).filter(models.User.id==id).first()
#     if not all_user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
#                              detail=f'user with id {id} not found')
#     return all_user

 
# @app.put('/user/{id}')            
# def update(id:int,request:schemas.User,db:Session=Depends(get_db)):
#     users=db.query(models.User).filter(models.User.id==id)
#     if not users.first():
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
#                              detail=f'User with id {id} not found')
#     users.update(request.dict())
    
#     db.commit()
#     db.refresh
#     return 'updated'

# @app.delete('/user/{id}')
# def destroy (id:int,db:Session=Depends(get_db)):
#     db.query(models.User).filter(models.User.id==id).delete(synchronize_session=False)
#     db.commit()
#     return 'deleted successfully'

    
# file upload
# @app.post("/file/upload")
# def file_bytes_len(file : bytes = File()):
#     return ({"file": len(file)})


# @app.post("/upload/file")
# def file_upload(file : UploadFile):
#     return ({"file_name": file.filename, "file_content_name": file.content_type})



    
    
    