from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import uuid
import os

from .config import settings
from .database import SessionLocal, init_db
from .models import User, SMSCode, RefreshToken, PasswordResetToken
from .schemas import (
    SendCodeRequest,
    VerifyPhoneRequest,
    EmailRegisterRequest,
    EmailLoginRequest,
    ForgotPasswordRequest,
    ResetPasswordRequest,
    AuthResponse,
    UserOut,
)
from .utils import hash_password, verify_password, create_access_token, create_refresh_token

init_db()
ROOT_PATH = os.getenv("ROOT_PATH", "/auth")
app = FastAPI(
    title="Auth Service",
    root_path=ROOT_PATH,
    docs_url=f"{ROOT_PATH}/docs" if ROOT_PATH else "/docs",
    redoc_url=f"{ROOT_PATH}/redoc" if ROOT_PATH else "/redoc",
    openapi_url=f"{ROOT_PATH}/openapi.json" if ROOT_PATH else "/openapi.json",
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/api/auth/phone/send-code")
def send_code(data: SendCodeRequest, db: Session = Depends(get_db)):
    now = datetime.utcnow()
    last_code = db.query(SMSCode).filter(SMSCode.phone == data.phone).order_by(SMSCode.sent_at.desc()).first()
    if last_code and (now - last_code.sent_at).total_seconds() < 30:
        raise HTTPException(status_code=429, detail="Too Many Requests")
    code = f"{uuid.uuid4().int % 1000000:06d}"
    sms = SMSCode(phone=data.phone, code=code, sent_at=now)
    db.add(sms)
    db.commit()
    # Placeholder: send SMS via provider
    return {"message": "Code sent"}


@app.post("/api/auth/phone/verify", response_model=AuthResponse)
def verify_phone(data: VerifyPhoneRequest, db: Session = Depends(get_db)):
    now = datetime.utcnow()
    sms = (
        db.query(SMSCode)
        .filter(SMSCode.phone == data.phone)
        .order_by(SMSCode.sent_at.desc())
        .first()
    )
    if not sms or (now - sms.sent_at).total_seconds() > 300 or sms.attempts >= 5:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired code")
    if sms.code != data.code:
        sms.attempts += 1
        db.commit()
        if sms.attempts >= 5:
            user = db.query(User).filter(User.phone == data.phone).first()
            if user:
                user.blocked_until = now + timedelta(hours=1)
                db.commit()
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired code")

    user = db.query(User).filter(User.phone == data.phone).first()
    if not user:
        if not data.email or not data.password:
            raise HTTPException(status_code=400, detail="Email and password required for registration")
        user = User(login_type="phone", phone=data.phone, email=data.email, is_active=True, password_hash=hash_password(data.password))
        db.add(user)
        db.commit()
    elif user.blocked_until and user.blocked_until > now:
        raise HTTPException(status_code=status.HTTP_423_LOCKED, detail="Phone temporarily blocked")
    sms.attempts = 0
    db.commit()
    access = create_access_token(user.id)
    refresh_value = create_refresh_token()
    refresh = RefreshToken(token=refresh_value, user_id=user.id, expires_at=now + timedelta(seconds=settings.refresh_token_ttl * (2 if data.remember_me else 1)))
    db.add(refresh)
    db.commit()
    return AuthResponse(access_token=access, refresh_token=refresh_value, user=UserOut(id=user.id, phone=user.phone, email=user.email, is_active=user.is_active))


@app.post("/api/auth/email/register")
def email_register(data: EmailRegisterRequest, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    token = str(uuid.uuid4())
    user = User(login_type="email", email=data.email, password_hash=hash_password(data.password), is_active=False, email_token=token, email_token_expires=datetime.utcnow() + timedelta(hours=24))
    db.add(user)
    db.commit()
    # Placeholder: send email with confirmation link containing token
    return {"message": "Confirmation sent"}


@app.get("/api/auth/email/confirm")
def email_confirm(token: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email_token == token, User.email_token_expires > datetime.utcnow()).first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    user.is_active = True
    user.email_token = None
    user.email_token_expires = None
    db.query(RefreshToken).filter(RefreshToken.user_id == user.id).delete()
    db.commit()
    return {"message": "Email confirmed"}


@app.post("/api/auth/email/login", response_model=AuthResponse)
def email_login(data: EmailLoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email, User.login_type == "email").first()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access = create_access_token(user.id)
    now = datetime.utcnow()
    refresh_value = create_refresh_token()
    refresh = RefreshToken(token=refresh_value, user_id=user.id, expires_at=now + timedelta(seconds=settings.refresh_token_ttl * (2 if data.remember_me else 1)))
    db.add(refresh)
    db.commit()
    return AuthResponse(access_token=access, refresh_token=refresh_value, user=UserOut(id=user.id, phone=user.phone, email=user.email, is_active=user.is_active))


@app.post("/api/auth/email/forgot")
def forgot_password(data: ForgotPasswordRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if user:
        token = str(uuid.uuid4())
        reset = PasswordResetToken(token=token, user_id=user.id, expires_at=datetime.utcnow() + timedelta(minutes=15))
        db.merge(reset)
        db.commit()
        # Placeholder: send email with reset token
    return {"message": "If email exists, reset link sent"}


@app.post("/api/auth/email/reset")
def reset_password(data: ResetPasswordRequest, db: Session = Depends(get_db)):
    reset = db.query(PasswordResetToken).filter(PasswordResetToken.token == data.token, PasswordResetToken.expires_at > datetime.utcnow()).first()
    if not reset:
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    user = db.query(User).filter(User.id == reset.user_id).first()
    user.password_hash = hash_password(data.new_password)
    db.query(RefreshToken).filter(RefreshToken.user_id == user.id).delete()
    db.delete(reset)
    db.commit()
    return {"message": "Password updated"}


@app.post("/api/auth/logout")
def logout(refresh_token: str, db: Session = Depends(get_db)):
    db.query(RefreshToken).filter(RefreshToken.token == refresh_token).delete()
    db.commit()
    return {"message": "Logged out"}
