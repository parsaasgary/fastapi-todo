import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi import status
from app.utils.reusable_testutils import client , setup_and_teardown , setup_and_teardown_user , auth_override
from app.Database.database import session 

from app.Database.model import User


def test_get_current_user(auth_override , setup_and_teardown_user):
    response = client.get("/user/me")
    data =response.json()

    assert response.status_code == status.HTTP_200_OK
    assert data["detail"] == "success"

    user_data = data["data"]
    assert user_data["username"] == "testuser"
    

def test_change_password (auth_override , setup_and_teardown_user):
    password_data = {"old_password" : "mypassword" , 
                     "new_password" : "changedpassword"}

    user_id = setup_and_teardown_user.id
    response = client.post(f"/user/change-password/{user_id}" , json=password_data)

    data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert data.get("detail") == "password updated successfully"

def test_change_password_fail (auth_override , setup_and_teardown_user):
    password_data = {"old_password" : "mypasswords312" , 
                     "new_password" : "changedpassword"}

    user_id = setup_and_teardown_user.id
    response = client.post(f"/user/change-password/{user_id}" , json=password_data)

    data = response.json()

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    