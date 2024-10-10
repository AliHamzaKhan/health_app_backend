from datetime import datetime, timedelta
from jose import jwt

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"

def generate_token(user_id: str) -> str:
    """
    Generates a JWT token for the authenticated user.
    """
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(hours=24)  # Token expiration time (24 hours in this case)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token