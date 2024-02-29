from .. import models, schemas, utils
from fastapi import FastAPI, Response, status, HTTPException,  Depends, APIRouter
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

# Users 
@router.post("/",  status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db:Session = Depends(get_db)):

    exist_user = db.query(models.User).filter(models.User.email == user.email).first()

    if exist_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail = f"user with email: {user.email} already exist")


    # Hash the password
    hash_password = utils.hash(user.password)
    user.password = hash_password
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}",response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} does not exist")

    return user