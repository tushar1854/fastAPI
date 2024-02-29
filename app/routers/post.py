from .. import models, schemas, oauth2
from fastapi import FastAPI, Response, status, HTTPException,  Depends, APIRouter
from ..database import get_db 
from sqlalchemy.orm import Session
from typing import List, Optional   
from sqlalchemy import func

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

# @router.get("/", response_model=List[schemas.Post])
@router.get("/",response_model=List[schemas.PostOut])
def test(db: Session = Depends(get_db),
         current_user: int = Depends(oauth2.get_current_user),
         limit: int= 10, skip: int = 0,
         search: Optional[str]= ""):
    
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # results = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(
    #     models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).all()
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    





    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db:Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    # new_post = models.Post(title=post.title, content=post.content, published= post.published)
    print(current_user.id)
    print(current_user.email)
    new_post = models.Post(owner_id= current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}", response_model=schemas.PostOut)
def get_specific_post(id:int, db:Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # post = db.query(models.Post).filter(models.Post.id == id).first()

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail= f"post with id: {id} was not found") 
    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db:Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id==id).first()
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail= f"post with id: {id} was not found") 
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    db.delete(post)
    # post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}")
def update_post(id:int, post:schemas.PostCreate, db:Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    # posta =post_query.first()
    if not post_query.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail= f"post with id: {id} was not found")

    if post_query.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()
    return{"message":"successfully updated"}