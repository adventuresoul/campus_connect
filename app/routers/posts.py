from fastapi import FastAPI, Depends, HTTPException, status, Response, APIRouter
from app import database, utils, schemas, models
from app.database import get_db
from app.Oauth2 import get_current_user
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from app.utils import convert_post_to_dict


router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

# special test route
@router.get("/test", response_model = schemas.Post)
def test(db: Session = Depends(get_db)): 
    posts = db.query(models.Post).all()
    return posts

# get all posts
@router.get("/")
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    posts_with_votes = db.query(models.Post, func.count(models.Vote.post_id)).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    posts_response = []
    for post, total_votes in posts_with_votes:
        post_dict = post.__dict__
        post_dict['total_votes'] = total_votes
        posts_response.append(post_dict)

    return posts_response

# get a single post
@router.get("/{id}", response_model = schemas.Post)
def get_post(id: int, db: Session = Depends(get_db), user = Depends(get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post:
        return post
    else:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with {id} not found")

# create a post
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), user = Depends(get_current_user)):
    # as per token the post will get updated with user_id
    new_post = models.Post(title = post.title, content = post.content, published = post.published, user_id = user.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)    # returning * in postgresql
    return new_post

# delete a post
@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), user = Depends(get_current_user)):  
    post_query = db.query(models.Post).filter(models.Post.id == id)
    # if post doesn't exists, raise exception
    if not post_query.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Post with id = {id} not found")
    # if the current user is not authorized as per token
    if post_query.first().user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied for requested action")
    # if found delete
    post_query.delete(synchronizes_session=False)
    db.commit()      
    return Response(status_code = status.HTTP_204_NO_CONTENT)

# Update a post
@router.put("/{id}", status_code = status.HTTP_200_OK, response_model = schemas.Post)
def update_post(id: int, updated_post: schemas.PostUpdate, db: Session = Depends(get_db), user = Depends(get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id = {id} not found")
    # if the current user is not authorized as per token
    if post_query.first().user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied for requested action")
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()








