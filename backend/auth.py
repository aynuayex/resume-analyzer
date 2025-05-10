import os
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, HTTPException
from jose import jwt
from pydantic import BaseModel

router = APIRouter() 

SECRET_KEY = os.getenv("JWT_SECRET")
ALGORITHM = "HS256"

class LoginInput(BaseModel):
    username: str
    password: str


@router.post("/login")
def login(data: LoginInput):
    if data.username != "admin" or data.password != "password":
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = jwt.encode(
        {"sub": data.username, "exp": datetime.now(timezone.utc) + timedelta(hours=1)},
        SECRET_KEY,
        algorithm=ALGORITHM,
    )
    return {"access_token": token}