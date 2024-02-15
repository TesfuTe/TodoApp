from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path
from starlette import status
from pydantic import BaseModel, Field
from passlib.context import CryptContext
from models import Users
from database import SessionLocal
from .auth import get_current_user


router = APIRouter(
    prefix='/user',
    tags=['user']
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class PasswordChangeRequest(BaseModel):
    password: str
    new_password: str = Field(min_length=6)


class PhonenumberChangeRequest(BaseModel):
    phone_number: str = Field(min_length=10, max_length=10)


@router.get("/", status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency, db: db_dependency):

    if user is None:
        raise HTTPException(status_code=401, detail="User not found.")

    return db.query(Users).filter(Users.id == user.get('id')).first()


@router.put("/change_password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user: user_dependency, db: db_dependency, passwordchange_request: PasswordChangeRequest):
    if user is None:
        raise HTTPException(status_code=401, detail="User not authenticated!")

    user_model = db.query(Users).filter(Users.id == user.get('id')).first()

    if not bcrypt_context.verify(passwordchange_request.password, user_model.hashed_password):
        raise HTTPException(
            status_code=401, detail="Error on change password.")

    user_model.hashed_password = bcrypt_context.hash(
        passwordchange_request.new_password)

    db.add(user_model)
    db.commit()


@router.put("/update_phone_number", status_code=status.HTTP_204_NO_CONTENT)
async def update_phone_number(user: user_dependency, db: db_dependency, phonenumber_change_request: PhonenumberChangeRequest):
    if user is None:
        raise HTTPException(status_code=401, detail="User not authenticated!")

    user_model = db.query(Users).filter(Users.id == user.get('id')).first()

    user_model.phone_number = phonenumber_change_request.phone_number

    db.add(user_model)
    db.commit()
