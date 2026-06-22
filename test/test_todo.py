import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi import status
from app.utils.reusable_testutils import client , setup_and_teardown , setup_and_teardown_user , auth_override
from app.Database.database import session 

from app.Database.model import TODO




def test_get_all_todos(setup_and_teardown):

        response = client.get("/todo/all_todos")
        data = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert data.get("detail") == "success"



def test_get_todo_by_id(setup_and_teardown):

        todo_id = setup_and_teardown.id
        response = client.get(f"/todo/todo/{todo_id}")
        data = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert data.get("detail") == "success"



def test_not_get_todo_by_id(setup_and_teardown):

        todo_id = 400
        response = client.get(f"/todo/{todo_id}")
        data = response.json()
        assert response.status_code == status.HTTP_404_NOT_FOUND



def test_add_new_todo(setup_and_teardown):
    
        new_todo_data = {
            "title": "Test Todo",
            "description": "This is a test todo",
            "priority" : 3 , 
            "complete": False
        }
        response = client.post("/todo/add-todo", json=new_todo_data)
        data = response.json()
        assert response.status_code == status.HTTP_201_CREATED
        assert data.get("detail") == "success"

        with session() as db:

            test_data = db.query(TODO).filter(TODO.title == "Test Todo").first()
            print(test_data)

            assert test_data.description == "This is a test todo"




def test_edit_todo(setup_and_teardown):

        todo_id = setup_and_teardown.id
        updated_todo_data = {
            "title": "Updated Test Todo",
            "description": "This is an updated test todo",
            "priority" : 2 , 
            "complete": True
        }
        response = client.put(f"/todo/update-todo/{todo_id}", json=updated_todo_data)
        data = response.json()
        assert response.status_code == status.HTTP_202_ACCEPTED
        assert data.get("detail") == "success"

        with session() as db:
            test_data = db.query(TODO).filter(TODO.title == "Updated Test Todo").first()
            assert test_data.description == "This is an updated test todo"


def test_delete_todo(setup_and_teardown):
      todo_id = setup_and_teardown.id

      response = client.delete(f"/todo/delete-todo/{todo_id}")

      assert response.status_code == status.HTTP_204_NO_CONTENT