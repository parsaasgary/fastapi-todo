from  pydantic import BaseModel , Field , ConfigDict
from typing import Optional


class UserPasswordChangeRequest(BaseModel):
    old_password : str = Field(... , description="the old password of the user" , examples=["123456"])
    new_password : str = Field(... ,min_length=6 ,max_length=50 ,description="the new password of the user" , examples=["12345678"])


    model_config = ConfigDict(
        json_schema_extra = {
            "example" : {
                "old_password" : "123456" ,
                "new_password" : "12345678"
            }
        }  
    )