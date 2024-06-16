from fastapi import FastAPI, Depends, HTTPException, status, Response, APIRouter, UploadFile, File, Form
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

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.User)
def create_user(username: str = Form(...),
                email: str = Form(...),
                password: str = Form(...), 
                db: Session = Depends(get_db)):
    # Hash the password
    hashed_pass = utils.password_hash(password)
    password = hashed_pass
    # Create a new user with profile picture
    new_user = models.User(username = username, email = email, password = password)
    # Add user to database
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")
    else:
        return new_user

@router.post("/profile", status_code=status.HTTP_201_CREATED, response_model=schemas.Message)
async def upload_profile(file: UploadFile = File(...), current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    contents = await file.read()
    # new photo obj
    new_profile = models.Profile(user_id = current_user.id, photo = contents)
    # save it to db
    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)
    return {"message": "Profile created succesfully"}

# query a user
@router.get("/{id}", response_model = schemas.User)
def get_user(id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    user = db.query(models.User).filter(models.User.id == id).first()
    # if user doesn't exist, raise Http error
    if not user:
        raise HTTPException(status_code =  status.HTTP_404_NOT_FOUND, detail = f"User with id = {id} not found")
    # else return the user
    return user