from pydantic import BaseModel


class SignupRequestDto(BaseModel):
    email: str
    password: str


class SignupResponseDto(BaseModel):
    access: str
    refresh: str


class LoginRequestDto(BaseModel):
    email: str
    password: str


class LoginResponseDto(BaseModel):
    access: str
    refresh: str


class RefreshResponseDto(BaseModel):
    access: str
    refresh: str
