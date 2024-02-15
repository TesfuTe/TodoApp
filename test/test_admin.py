from fastapi import status
from utils import *
from routers.admin import get_db, get_current_user
from models import Todos


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_admin_read_all_authenticated(test_todo):
    response = client.get("/admin/todo")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {'title': 'Learn Docker', 'priority': 5, 'description': 'Learn to get experience', 'owner_id': 1, 'complete': False, 'id': 1}]


def test_admin_delete_todo(test_todo):
    response = client.delete("/admin/delete/1")
    assert response.status_code == 204

    db = TestingSessionLocal()
    todo_model = db.query(Todos).filter(Todos.id == 1).first()

    assert todo_model is None


def test_admin_delete_todo_not_found(test_todo):
    response = client.delete("/admin/delete/8671")
    assert response.status_code == 404
    assert response.json() == {'detail': 'Todod not found.'}
