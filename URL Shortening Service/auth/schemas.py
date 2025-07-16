from pydantic import BaseModel


class UserRegister(BaseModel):
    username: str
    password: str


class UserRegisterResponse(BaseModel):
    message: str = "User registered succesfully!"


class UserLogin(BaseModel):
    username: str
    password: str


class UserLoginResponse(BaseModel):
    message: str = "Login Successful"
    token: str
