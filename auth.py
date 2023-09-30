from datetime import timedelta, datetime
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from starlette import status
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

SECRET_KEY = 'c90bacd9ba5d2bd54589318dddb1326883c16341e3badde22bb6e4f21f695d70'
ALGORITHM = 'HS256'

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

class CreateUserRequest(BaseModel):
    id: str
    username: str
    password: str
    is_admin: str

class Token(BaseModel):
    access_token: str
    token_type: str

def authenticate_user(username: str, password: str, client):
    data = client.command(f'SELECT * FROM USERS WHERE username=\'{username}\';')
    if not data:
        return False
    users_dict = {}
    i = 0
    while i < len(data) - 3:
        users_dict[data[i]] = {
            'id': data[i],
            'username': data[i + 1],
            'password': data[i + 2],
            'is_admin': data[i + 3],
        }
        i += 4
    if not bcrypt_context.verify(password, list(users_dict.values())[0]['password']):
        return False
    return list(users_dict.values())[0]

def create_access_token(username: str, is_admin: str, expires_delta: timedelta):
    encode = {'sub': username, 'bool': is_admin}
    expires = datetime.utcnow() + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(payload)
        print("--------------------------------")
        username: str = payload.get('sub')
        is_admin: str = payload.get('bool')
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not validate user.')
        return {'username': username,
                'is_admin': is_admin}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user.')

# @router.post("/auth", status_code=status.HTTP_201_CREATED)
# async def create_user(create_user_request: CreateUserRequest):
#     create_user_model = Users(
#         username=create_user_request.username,
#         hashed_password=bcrypt_context.hash(create_user_request.password)
#     )

#     client.command(f'INSERT INTO USERS VALUES (\'{create_user_request.username}\', \'{bcrypt_context.hash(create_user_request.password)}\');')