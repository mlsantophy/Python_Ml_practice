from fastapi import APIRouter,HTTPException,status,Depends
from mode.database import Session,engine
from schemas import SignUpModel,LogInModel
from mode.models import User
from mode import models
from werkzeug.security import generate_password_hash,check_password_hash
from fastapi_jwt_auth import AuthJWT
from fastapi.encoders import jsonable_encoder



router=APIRouter(
    prefix="/auth",
    tags=['auth']
)

session=Session(bind=engine)



@router.get('/')
def hello(Authorize:AuthJWT=Depends()):

   
    try:
        Authorize.jwt_required()

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token"
        )

    return {"message":"Hello World"}


@router.post("/signup",status_code=status.HTTP_201_CREATED)
def signup(user:SignUpModel):
    db_email=session.query(User).filter(User.email==user.email).first()

    if db_email is not None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with the email already exists"
        )

    db_username=session.query(User).filter(User.username==user.username).first()

    if db_username is not None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with the username already exists"
        )

    new_user=User(
        username=user.username,
        email=user.email,
        password=generate_password_hash(user.password),
        is_active=user.is_active,
        is_staff=user.is_staff
    )

    session.add(new_user)

    session.commit()

    return new_user


#login route
@router.post("/login",status_code=200)
def login(user:LogInModel,Authorize:AuthJWT=Depends()):
    db_user=session.query(User).filter(User.username==user.username).first()
    if db_user and check_password_hash(db_user.password,user.password):
        access_token=Authorize.create_access_token(subject=db_user.username)
        refresh_token=Authorize.create_refresh_token(subject=db_user.username)


        response={
            "access":access_token,
            "refresh":refresh_token
        }
        return jsonable_encoder(response)

    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                         detail="invalid username or password")


#refreshing token
@router.get('/refresh')
def refresh_token(Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_refresh_token_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
               detail="please provide a valid token")
    
    current_user=Authorize.get_jwt_subject()

    access_token=Authorize.create_access_token(subject=current_user)

    return jsonable_encoder({"access":access_token})           
                         