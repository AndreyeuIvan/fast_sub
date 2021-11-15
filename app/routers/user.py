from fastapi import APIRouter, status, Response, Depends, HTTPException
from sqlalchemy.orm import Session

from ..schemas import UserOut, UserCreate
from ..models import User
from ..db import get_db


router = APIRouter(
    prefix='/users',
    tags=['Users']
)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    hash_pass = hash(user.password)
    user.password = hash_pass
    new_user = User(
        **user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get('/{_id}', response_model=UserOut)
def get_user(_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == _id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with id: {_id} does not exist')
    return user
