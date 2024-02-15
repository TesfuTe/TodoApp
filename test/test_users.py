from fastapi import status
from utils import *
from models import Users
from routers.users import get_db, get_current_user
from routers.auth import bcrypt_context

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_get_user(test_user):
    response = client.get("/user")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['username'] == "user"
    assert response.json()['email'] == "user@gmail.com"
    assert response.json()['first_name'] == "User"
    assert response.json()['last_name'] == "User"
    # assert response.json()['hashed_password'] == bcrypt_context.hash(
    #     "testpass1")
    assert response.json()['role'] == "admin"
    assert response.json()['phone_number'] == "0707070707"


def test_change_password_success(test_user):
    response = client.put(
        "/user/change_password", json={"password": "testpass", "new_password": "newtestpass"})
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_change_password_invalid_current_password(test_user):
    response = client.put(
        "/user/change_password", json={"password": "testpass1", "new_password": "newtestpass"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail': 'Error on change password.'}


def test_change_phone_number_success(test_user):
    response = client.put(
        "/user/update_phone_number", json={"phone_number": "0808080808"})
    assert response.status_code == status.HTTP_204_NO_CONTENT
