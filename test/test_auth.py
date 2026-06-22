import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi import status , HTTPException
from app.utils.reusable_testutils import client , setup_and_teardown , setup_and_teardown_user , auth_override
from app.Database.database import session 

from app.Database.model import User

from app.utils.jwt import create_access_token , verify_token

from app.utils.authentication import get_current_user

import pytest

def test_add_new_user(  setup_and_teardown_user):
    new_user = {
        "email" : "mytestemail2@gmail.com" ,
        "username" : "testuser2" ,
        "name" : "test2" ,
        "lastname" : "dummy2" ,
        "password" : "mypassword123",
        "role" : "admin" 
    }

    response = client.post("/auth/add_user" , json=new_user)

    data = response.json()

    assert response.status_code == status.HTTP_201_CREATED
    assert data.get("detail") == "user created successfully"




def test_get_token(setup_and_teardown_user):

    user_info = {
        "username": setup_and_teardown_user.username,
        "password": "mypassword"
    }

    response = client.post("/auth/Token", data=user_info)

    data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert data.get("token_type") == "bearer"



def test_get_wrong_token(setup_and_teardown_user):

    user_info = {
        "username": setup_and_teardown_user.username,
        "password": "mypassword123"
    }

    response = client.post("/auth/Token", data=user_info)

    data = response.json()

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_create_token_valid(setup_and_teardown_user):

    data = {
        "sub" : setup_and_teardown_user.username ,
        "id"  : setup_and_teardown_user.id ,
    }

    token = create_access_token(data=data)

    encoded_token = verify_token(token=token)

    assert encoded_token.get("username") == "testuser"

    assert encoded_token.get("id") == setup_and_teardown_user.id




def test_get_current_user_valid(setup_and_teardown_user):
    data = {
        "sub" : setup_and_teardown_user.username ,
        "id"  : setup_and_teardown_user.id ,
    }

    token =  create_access_token(data=data)

    user = get_current_user(token=token)

    assert user.get("username") == "testuser"

    assert user.get("id") == setup_and_teardown_user.id


def test_get_current_user_invalid(setup_and_teardown_user):
    data = {
        "sub" : setup_and_teardown_user.username ,

    }

    token =  create_access_token(data=data)

    with pytest.raises(HTTPException) as excep:
        get_current_user(token=token)

    assert excep.value.status_code == 401
    assert excep.value.detail == "Could not validate credentials"





