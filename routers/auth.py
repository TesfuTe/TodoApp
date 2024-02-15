from typing import Annotated
from fastapi import Depends, FastAPI, APIRouter, Path, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from starlette import status
from pydantic import BaseModel
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta
from database import SessionLocal
from models import Users


router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

SECRET_KEY = '13c3b7201bc6095d0f929be55a99258df10d2e672a13b1aba8d1bea2b1869961'
ALGORITHM = 'HS256'


class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str
    phone_number: str


class Token(BaseModel):
    access_token: str
    token_type: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


def authenticate_user(username: str, password: str, db):
    user = db.query(Users).filter(Users.username == username).first()

    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user


def create_access_token(username: str, user_id: int, role: str, expires_delta: timedelta):

    expires = datetime.utcnow() + expires_delta
    encode = {'sub': username, 'id': user_id, 'exp': expires, 'role': role}

    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: str = payload.get('id')
        user_role: str = payload.get('role')
        if username is None or user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user.")
        return {'username': username, 'id': user_id, 'user_role': user_role}
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user.")


@router.get("/users", status_code=status.HTTP_200_OK)
async def get_all_users(db: db_dependency):
    users_list = db.query(Users).all()

    if users_list is not None:
        return users_list
    raise HTTPException(status_code=404, detail="No users found")


@router.get("/users/{user_id}", status_code=status.HTTP_200_OK)
async def get_user_by_id(db: db_dependency, user_id: int = Path(gt=0)):
    user = db.query(Users).filter(Users.id == user_id).first()

    if user is not None:
        return user
    raise HTTPException(status_code=404, detail="User not found.")


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: CreateUserRequest):
    create_user_model = Users(
        email=create_user_request.email,
        username=create_user_request.username,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        role=create_user_request.role,
        phone_number=create_user_request.phone_number,
        hashed_password=bcrypt_context.hash(create_user_request.password),
        is_active=True
    )

    # return create_user_model
    db.add(create_user_model)
    db.commit()


@router.post("/token", response_model=Token)
async def login_for_access_token(from_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 db: db_dependency):
    user = authenticate_user(from_data.username, from_data.password, db)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user.")
    user_token = create_access_token(
        user.username, user.id, user.role, timedelta(minutes=20))
    return {'access_token': user_token, 'token_type': 'bearer'}
