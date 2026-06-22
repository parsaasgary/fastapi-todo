from app.Database.model import TODO
from sqlalchemy.orm import Session


def get_todos(database : Session, user_id: int):

    return database.query(TODO).filter(TODO.owner_id == user_id).all()

def todo_by_id(database : Session , todoID, user_id: int):
    return database.query(TODO).filter(TODO.id == todoID, TODO.owner_id == user_id).first()


def create_todo(database : Session , todo : TODO):
    database.add(todo)
    database.commit()
    database.refresh(todo)
    return todo

def update_todo (database : Session , todoID , data : dict , user_id: int):
    todo_to_update = database.query(TODO).filter(TODO.id == todoID, TODO.owner_id == user_id).first()
    if not todo_to_update:
        return None
    for key, value in data.items():
        setattr(todo_to_update, key, value)
    database.commit()
    database.refresh(todo_to_update)
    return todo_to_update

def delete_todo(database: Session , todoID, user_id: int):
    todo_to_delete = database.query(TODO).filter(TODO.id == todoID, TODO.owner_id == user_id).first()
    if not todo_to_delete:
        return None
    database.delete(todo_to_delete)
    database.commit()
    return todo_to_delete