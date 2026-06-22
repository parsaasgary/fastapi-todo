from fastapi import APIRouter , Depends , Response , status , HTTPException , Path

from app.Database.database import engine , session
from sqlalchemy.orm import Session
from app.services.todos.todo_CRUD import  get_todos , todo_by_id , create_todo , update_todo , delete_todo
from app.Database import model

from .todo_schema import TodoSendData , TodoEditData

from app.utils.authentication import get_current_user

router = APIRouter(
    prefix= "/todo" ,
    tags = ["todos"]
)

# create a database interaction function
def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()



# get all todos
@router.get("/all_todos" ,
         responses={
             "200" : {"description" : "all todos retrive"} ,
             "500" : {"description" : "internal server erros"}
         } ,
         )
def get_all_todos(response : Response , db : Session = Depends(get_db) , user : dict = Depends(get_current_user) ):
    try:
        data = get_todos(database= db , user_id = user.get("id"))
        response.status_code = status.HTTP_200_OK   
        return {
            "detail" : "success" , 
            "data" : data ,
        }
    
    except Exception as e:

        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return{
            "detail" : "failed"
        }


@router.get("/todo/{todo_id}" ,
         responses= {
             "200" : {"description" : "retrive the todo by the id"} ,
             "500" : {"description" : "internal server error . databse unreachable"}
         },
         )
def get_todo_by_id( response : Response , db : Session = Depends(get_db) , todo_id : int = Path(gt=0) , user : dict = Depends(get_current_user) ):
    try:
        data = todo_by_id(db , todo_id , user_id = user.get("id"))
        response.status_code = status.HTTP_200_OK
        return {
            "detail" : "success" ,
            "data" : data
        }
    except Exception as e : 
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        raise HTTPException(status_code=response.status_code , detail= " internal server error")
    

@router.post("/add-todo")
async def add_a_todo(todo : TodoSendData ,
                    response : Response ,
                    db : Session = Depends(get_db) ,
                    user : dict = Depends(get_current_user) ):
    try:
        if not user:
            response.status_code = status.HTTP_401_UNAUTHORIZED
            raise HTTPException(status_code=response.status_code , detail= f"unauthorized access")
        print(user)
        new_todo = model.TODO(**todo.dict() , owner_id = user.get("id"))
        new_todo = create_todo(db , new_todo)
        response.status_code = status.HTTP_201_CREATED
        return {
            "detail" : "success" ,
            "data" : new_todo
        }
    except Exception as e :
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        raise HTTPException(status_code=response.status_code , detail= f" internal server error{str(e)}")
    
@router.put("/update-todo/{todo_id}")
async def update_a_todo(todo : TodoEditData ,
                        response : Response ,
                        db : Session = Depends(get_db),
                        todo_id : int = Path(gt=0) ,
                        user : dict = Depends(get_current_user) ):
    try:
        todo_to_update = update_todo(db , todo_id , todo.dict(exclude_unset=True) , user.get("id"))
        if not todo_to_update :
            response.status_code = status.HTTP_404_NOT_FOUND
            raise HTTPException(status_code=response.status_code , detail= "todo not found")

        response.status_code = status.HTTP_202_ACCEPTED
        return {
            "detail" : "success" ,
            "data" : todo_to_update
        }
    except HTTPException as e :
        raise e
    except Exception as e :
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        raise HTTPException(status_code=response.status_code , detail= f" internal server error{str(e)}")
    

@router.delete("/delete-todo/{todo_id}")
async def delete_a_todo( response : Response , 
                        db : Session = Depends(get_db) , 
                        todo_id : int = Path(gt=0) , 
                        user : dict = Depends(get_current_user)):
    try:
        deleted_todo = delete_todo(db , todo_id, user.get("id"))
        if not deleted_todo :
            response.status_code = status.HTTP_404_NOT_FOUND
            raise HTTPException(status_code=response.status_code , detail= "todo not found")

        response.status_code = status.HTTP_204_NO_CONTENT
        return {
            "detail" : "success" ,
            "data" : deleted_todo
        }
    except HTTPException as e :
        raise e
    except Exception as e :
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        raise HTTPException(status_code=response.status_code , detail= f" internal server error{str(e)}")