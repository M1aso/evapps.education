from datetime import datetime
from pydantic import BaseModel, EmailStr, constr

class SendCodeRequest(BaseModel):
    phone: constr(regex=r'^\+7\d{10}$')

class VerifyPhoneRequest(BaseModel):
    phone: constr(regex=r'^\+7\d{10}$')
    code: constr(min_length=6, max_length=6)
    email: EmailStr | None = None
    password: str | None = None
    remember_me: bool = False

class EmailRegisterRequest(BaseModel):
    email: EmailStr
    password: str

class EmailLoginRequest(BaseModel):
    email: EmailStr
    password: str
    remember_me: bool = False

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class UserOut(BaseModel):
    id: str
    phone: str | None = None
    email: str | None = None
    is_active: bool

class AuthResponse(TokenResponse):
    user: UserOut
