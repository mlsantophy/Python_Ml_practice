from typing import List
from fastapi import APIRouter, Depends,status,HTTPException,File,UploadFile,BackgroundTasks
from .. import schemas, database,models,oauth2
from sqlalchemy.orm import Session

router=APIRouter(tags=['file'])

get_db=database.get_db


@router.post("/file/upload")
def file_bytes_len(file : bytes = File(),current_user:schemas.User=Depends(oauth2.get_current_user)):
    return ({"file": len(file)})


@router.post("/upload/file")
def file_upload(file : UploadFile,current_user:schemas.User=Depends(oauth2.get_current_user)):
    return ({"file_name": file.filename, "file_content_name": file.content_type})

