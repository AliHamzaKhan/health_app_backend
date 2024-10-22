import secrets
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError

SECRET_KEY = secrets.token_hex(32)
ALGORITHM = "HS256"

def generate_token(user_id: str) -> str:
    """
    Generates a JWT token for the authenticated user.
    """
    payload = {
        "user_id": user_id,
        "exp": datetime.now(timezone.utc) + timedelta(weeks=4)  # Token expiration time (24 hours in this case)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token


def decode_token(token: str) -> str:
    """
    Decodes the JWT token and returns the user_id if valid.
    """
    print('token',token)
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        return payload.get("user_id")  # Returns the user_id from the token payload
    except JWTError:
        raise Exception("Invalid token or token has expired")


