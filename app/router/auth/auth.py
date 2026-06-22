from datetime import datetime, timedelta, timezone
from urllib import response
from fastapi import APIRouter , Depends, Form , Response , status , HTTPException , Path
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.Database.database import session

from app.services.auth.auth_CRUD import create_new_user , user_login

from app.utils.password import hash_password  
from app.utils.jwt import create_access_token 

from .auth_schema import CreateUserRequest , Token



router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

# create a database interaction function
def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()
        
@router.post("/add_user")
def add_new_user(user : CreateUserRequest , database : Session = Depends(get_db) , response : Response = None):
    try:
        new_user = create_new_user(database= database , user_data= user)
        response.status_code = status.HTTP_201_CREATED
        return {
            "detail" : "user created successfully" ,
            "newly created user id" : new_user.id
        }
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            "detail" : "failed to create the user"
        }

@router.post("/Token")
async def login_for_access_token(username : str = Form(...) , password : str = Form(...) ,
                                database : Session = Depends(get_db) ,
                                response : Response = None)->Token:
    try:
        user = user_login(database= database , username = username , password = password)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="invalid username or password")
        # Create an access token
        access_token = create_access_token(data={"sub": user.username ,
                                                 "id" : user.id ,
                                                "exp" : datetime.now(timezone.utc) + timedelta(minutes=10)
                                                }
                                            )
        response.status_code = status.HTTP_200_OK
        return Token(access_token=access_token, token_type="bearer")

    except HTTPException:
        raise
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occurred during login")