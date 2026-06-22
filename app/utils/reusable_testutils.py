from fastapi.testclient import TestClient
import pytest
from app.Database.database import session , engine 
from app.main import app
from app.Database.model import TODO , User

from sqlalchemy import text

from app.utils.authentication import get_current_user as auth_get_current_user

from .password import hash_password




client = TestClient(app)



@pytest.fixture
def setup_and_teardown_user():

    my_user = User(
        email = "mytestemail@gmail.com" ,
        username = "testuser" ,
        name = "test" ,
        lastname = "dummy" ,
        hash_password = hash_password("mypassword") ,
        role = "admin" 
    )

    db = session()
    db.add(my_user)
    db.commit()
    db.refresh(my_user)

    yield my_user
    db.query(User).delete()
    db.commit()
    db.close()


@pytest.fixture
def auth_override(setup_and_teardown_user):
    def _override():
        return {
            "username": setup_and_teardown_user.username,
            "id": setup_and_teardown_user.id   # ✅ REAL ID
        }

    app.dependency_overrides[auth_get_current_user] = _override
    yield
    app.dependency_overrides.clear()


@pytest.fixture()
def setup_and_teardown(auth_override , setup_and_teardown_user):
    # Setup code before each test
    my_todo = TODO(title="Test Todo",
                description="This is a test todo",
                priority=1,
                complete=False ,
                owner_id =setup_and_teardown_user.id )
    
    db = session()
    db.add(my_todo)
    db.commit()
    db.refresh(my_todo)

    yield my_todo  # This is where the test function will run


    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todo"))
        connection.commit()

