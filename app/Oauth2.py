from jose import JWTError, jwt
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from fastapi import Depends, status, HTTPException
from app.models import User
from app.database import get_db
from fastapi.security import OAuth2PasswordBearer
import os
from dotenv import load_dotenv

# load env variables
load_dotenv()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = os.getenv("secret_key")
ALGORITHM = os.getenv("algorithm")
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# data will contain username 
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # to the data dict add another field expire
    to_encode.update({"exp": expire})
    # encode the token using SECRET_KEY
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    # after encoding send the token
    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    try:
        # decode function takes header and payload of token and creates a signature using secret_key 
        # and tries to match it with token's signature and verifies. It also looks for expiration time and raises an error
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        userid: str = payload.get("user_id")
        if userid is None:
            raise credentials_exception
        # model the id into TokenData scheme
        # token_data = TokenData(userid)
    except JWTError:
        raise credentials_exception
    # if no error occurs, return token_data: in the sense, user_id
    return userid

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail=f"Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})

    # get the token and send it to verify function
    userid = verify_access_token(token, credentials_exception)
    # upon successfull verification of token, query the user as per token data
    user = db.query(User).filter(User.id == userid).first()
    # return the user id
    return user