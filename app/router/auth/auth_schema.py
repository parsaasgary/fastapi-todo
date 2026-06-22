from pydantic import BaseModel , Field , ConfigDict
from typing import Optional

class CreateUserRequest(BaseModel):
    email : str = Field(... , description="the email of the user" , examples=["example@example.com"])
    username : str = Field(... , description="the username of the user" , examples=["parsaasgary"])
    name : str = Field(... , description="the name of the user" , examples=["parsa"])
    lastname : str = Field(... , description="the lastname of the user" , examples=["asgary"])
    password : str = Field(... , description="the password of the user" , examples=["strongpassword123"])
    role : str = Field(... , description="the role of the user" , examples=["admin" , "user"])

    model_config = ConfigDict(
        json_schema_extra = {
            "example" : {
                "email" : "example@example.com",
                "username" : "parsaasgary",
                "name" : "parsa",
                "lastname" : "asgary",
                "password" : "strongpassword123",
                "role" : "user"
            }
        }
    )

class Token(BaseModel):
    access_token: str
    token_type: str
