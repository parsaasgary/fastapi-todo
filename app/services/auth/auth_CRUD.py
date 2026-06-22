import email

from app.Database.model import User
from sqlalchemy.orm import Session
from app.router.auth.auth_schema import CreateUserRequest
from app.utils.password import hash_password, verify_password

def user_login(database : Session , username : str , password : str):
    user = database.query(User).filter(User.username == username).first()
    
    # ADD THESE PRINTS TO DEBUG
    print(f"DEBUG: Input Password Length: {len(password)}")
    print(f"DEBUG: Stored Hash: {user.hash_password if user else 'User not found'}")
    
    if user and verify_password(password , user.hash_password):
        return user
    return None


def create_new_user (database : Session , user_data : CreateUserRequest):
    user_data.password = hash_password(user_data.password)
    new_user = User(
        email = user_data.email ,
        username = user_data.username ,
        name = user_data.name ,
        lastname = user_data.lastname ,
        hash_password = user_data.password ,
        role = user_data.role , 
        is_active = True
    )
    database.add(new_user)
    database.commit()
    database.refresh(new_user)
    return new_user



