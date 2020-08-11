from pydantic import BaseModel

class RegisterRequest(BaseModel):
    username : str
    password : str

class LoginRequest(BaseModel):
    username : str
    password : str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str = None