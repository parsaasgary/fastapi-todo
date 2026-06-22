from fastapi import APIRouter, Body , Depends , Response , status , HTTPException , Path

from app.services.user.user_service import change_user_password

from app.Database.database import engine , session
from sqlalchemy.orm import Query, Session

from .user_schema import UserPasswordChangeRequest


from app.utils.authentication import get_current_user

router = APIRouter(
    prefix= "/user" ,
    tags = ["user"]
)

# create a database interaction function
def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()

@router.get("/me")
def get_current_user_info( response : Response , user : dict = Depends(get_current_user)):
    try:
        response.status_code = status.HTTP_200_OK
        return {
            "detail" : "success" ,
            "data" : user
        }
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        raise HTTPException(status_code=response.status_code , detail= f" internal server error{str(e)}")
    

@router.post("/change-password/{user_id}")
def change_password(
                    password_data : UserPasswordChangeRequest ,
                    response : Response , 
                    db : Session = Depends(get_db) , 
                    user_id : int = Path(gt=0) , 
                    user : dict = Depends(get_current_user),
                    ):

        if user.get("id") != user_id:
            response.status_code = status.HTTP_403_FORBIDDEN
            raise HTTPException(status_code=response.status_code , 
                                detail= "you are not allowed to change this password")
        
        updated_user_password = change_user_password(db , user_id , password_data.new_password , password_data.old_password)
        response.status_code = status.HTTP_200_OK
        return {
            "detail" : "password updated successfully"
        }
