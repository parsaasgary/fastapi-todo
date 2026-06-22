from  pydantic import BaseModel , Field , ConfigDict
from typing import Optional


class TodoSendData(BaseModel):
    title : str = Field(... , description="the title of the todo" , examples=["buy dog food"])
    description : str = Field(... ,min_length=5 ,max_length=50 ,description="small title about the job" , examples=["i had a misscall from my dad"])
    priority : int = Field(... ,gt=0, lt=6 , description="how importatnt it is . 1 highest , 5 lowest" )
    complete : bool = Field (... , description="is it done or not?" , examples=[False])


    model_config = ConfigDict(
        json_schema_extra = {
            "example" : {
                "title" : "buy dog food" ,
                "description" : "i had a misscall from my dad" ,
                "priority" : 1 ,
                "complete" : False
            }
        }  
    )


class TodoEditData(BaseModel):
    title : Optional[str] = Field(None , description="the title of the todo" , examples=["buy dog food"])
    description : Optional[str]  = Field(None ,min_length=5 ,max_length=50 ,description="small title about the job" , examples=["i had a misscall from my dad"])
    priority : Optional[int]  = Field(None ,gt=0, lt=6 , description="how importatnt it is . 1 highest , 5 lowest" )
    complete : Optional[bool] = Field (None , description="is it done or not?" , examples=[False])