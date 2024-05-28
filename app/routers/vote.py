from fastapi import FastAPI, Depends, HTTPException, status, Response, APIRouter
from app import database, utils, schemas, models
from app.database import get_db
from sqlalchemy.orm import Session
from typing import List
from app.Oauth2 import get_current_user

router = APIRouter(
    prefix="/vote",
    tags=["Vote"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def update_vote(vote: schemas.Vote, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    # Check if post exists
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with post_id {vote.post_id} does not exist")
    # Vote query
    vote_query = db.query(models.Vote).filter(models.Vote.user_id == current_user.id, models.Vote.post_id == vote.post_id)
    # Get the first instance and if vote already exists raise HTTPException
    present_vote_instance = vote_query.first()
    # According to the pydantic model
    if vote.vote_value == 1:
        if present_vote_instance:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Vote with user_id = {current_user.id} for post_id = {vote.post_id} already exists")
        
        # If the current user has not voted
        new_vote = models.Vote(user_id=current_user.id, post_id=vote.post_id)
        db.add(new_vote) 
        db.commit()
        return {"message": "Successfully voted"}
    elif vote.vote_value == 0:
        if not present_vote_instance:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Vote does not exist")
        
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "Successfully deleted vote"}
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid vote_value")
