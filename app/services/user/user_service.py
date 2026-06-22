from app.Database.model import User
from sqlalchemy.orm import Session
from app.router.auth.auth_schema import CreateUserRequest
from app.utils.password import hash_password, verify_password

from fastapi import  status , HTTPException  

def change_user_password(db : Session , user_id : int , new_password : str , old_password : str):
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    if not verify_password(old_password, user.hash_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid old password")
    
    user.hash_password = hash_password(new_password)
    db.commit()
    db.refresh(user)
    return user