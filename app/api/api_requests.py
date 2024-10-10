from fastapi import FastAPI, UploadFile, File, Form, Header, HTTPException, Depends
# from fastapi.responses import JSONResponse
from jose import JWTError, jwt
from pydantic import BaseModel
from typing import Optional, Dict
from starlette.responses import JSONResponse
from app.models.user_profile import UserProfile


SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"

# Mock database for profiles


class Profile(BaseModel):
    name: str
    email: str
    age: int


def decode_jwt(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload  # return token data if valid
    except JWTError:
        return None


# Dependency to verify the token
def verify_token(auth_token: Optional[str] = Header(None)):
    if not auth_token:
        raise HTTPException(status_code=403, detail="Authorization token missing")

    # Split the Bearer token
    token_parts = auth_token.split()
    if len(token_parts) != 2 or token_parts[0].lower() != "bearer":
        raise HTTPException(status_code=403, detail="Invalid token format")

    token = token_parts[1]
    payload = decode_jwt(token)
    if payload is None:
        raise HTTPException(status_code=403, detail="Invalid or expired token")

    return payload

