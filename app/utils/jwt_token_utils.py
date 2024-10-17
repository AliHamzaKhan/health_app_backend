from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"

# Function to verify the token
def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        # Decode the JWT token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return {"user_id": user_id}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


@app.get("/protected")
async def protected_route(user: dict = Depends(verify_token)):
    return {"message": f"Hello, user {user['user_id']}! You are authorized to access this route."}
