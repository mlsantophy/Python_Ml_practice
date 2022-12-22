from fastapi import APIRouter,Depends, status,HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from .. import schemas, database, models,token,oauth2
from ..hashing import Hash
from sqlalchemy.orm import Session

router=APIRouter(tags=['authentication'])

get_db=database.get_db

@router.post('/login')
def login(request:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(database.get_db),current_user:schemas.User=Depends(oauth2.get_current_user)):
    user=db.query(models.User).filter(models.User.email==request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid Credential")
    if not Hash.verify(user.password,request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Incorrect password")
        
    access_token=token.create_access_token(data={"sub":user.email})
    return {"access_token":access_token,"token_type":'bearer'}    
