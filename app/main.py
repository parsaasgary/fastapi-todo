from fastapi import FastAPI 


from app.router.user.user import router as user_router
from app.router.auth.auth import router as auth_router
from app.router.todos.todo import router as todo_router


app = FastAPI()

@app.get("/")
def health_check():
    return {"detail" : "api is fine"}

app.include_router(auth_router)
app.include_router(todo_router)
app.include_router(user_router)

