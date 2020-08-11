import hashlib
import uuid
from models.accounts import (
    User,
    UserInDB,
    )
import jwt 
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt import PyJWTError
from datetime import datetime, timedelta
from db.mongodb import get_nosql_db
from pydantic import BaseModel
from fastapi import Depends, FastAPI, HTTPException, status
from pymongo.errors import DuplicateKeyError
from starlette.responses import JSONResponse
from core import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str = None

def create_user(request):
    salt = uuid.uuid4().hex
    hashed_password = hashlib.sha512(str(request.password+salt).encode('utf-8')).hexdigest()
    user = {}
    user['username'] = request.username
    user['password'] = hashed_password
    user['salt'] = salt
    user = User(**user)
    print(user)
    return user



async def get_user(username: str):
    client = await get_nosql_db()
    users_db = client[settings.MONGODB_NAME]["user"]
    row = await users_db.find_one({"username":username})
    if row is not None:
        return UserInDB(**row)
    else:
        return None

def verify_password(plain_password, password):
    checked_password = hashlib.sha512(plain_password.encode("utf-8")).hexdigest()
    return checked_password == password

async def authenticate_user(username: str, password: str):
    user = await get_user(username)
    if not user:
        return False
    if not verify_password((password+user.salt), user.password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode,settings.SECRET_KEY, algorithm=settings.ALGORITHM).decode('utf-8')
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithm=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except PyJWTError as e:
        print(e)
        raise credentials_exception
    user = await get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    return current_user


