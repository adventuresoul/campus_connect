from fastapi import FastAPI, Depends, HTTPException, status, Response, APIRouter
from app import database, utils, schemas, models
from app.database import get_db
from sqlalchemy.orm import Session
from app.Oauth2 import get_current_user
from typing import List

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

### Users route
@router.get("/", response_model = List[schemas.UserBase])
def get_users(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    users = db.query(models.User).all()
    return users

# create a user
@router.post("/", status_code = status.HTTP_201_CREATED, response_model = schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_pass = utils.password_hash(user.password)
    user.password = hashed_pass
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)    # returning * in postgresql
    return new_user

# query a user
@router.get("/{id}", response_model = schemas.User)
def get_user(id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    user = db.query(models.User).filter(models.User.id == id).first()
    # if user doesn't exist, raise Http error
    if not user:
        raise HTTPException(status_code =  status.HTTP_404_NOT_FOUND, detail = f"User with id = {id} not found")
    # else return the user
    return user
