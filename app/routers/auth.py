from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.Oauth2 import create_access_token
from app.utils import validate
from app.schemas import UserLogin, Token
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(
    tags=["Authentication"]
)

@router.post("/login", status_code=status.HTTP_200_OK, response_model=Token)
def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    #check if the user exists in db, since
    user = db.query(User).filter(User.email == user_credentials.email).first()
    # if user doesn't exists, raise Http Error
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    # check the password
    # print(user_credentials.password, user.password)
    if not validate(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN , detail=f"Invalid Credentials")
    # if everything works fine, return the token
    access_token = create_access_token(data = {"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}
