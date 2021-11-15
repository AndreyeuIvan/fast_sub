from fastapi import APIRouter, status, Response, Depends, HTTPException
from sqlalchemy.orm import Session

from ..schemas import EpisodeS, EpisodeCreate
from ..models import Episode
from ..db import get_db

router = APIRouter(
    prefix="/episode",
    tags=['episode']
)


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_episode(episode: EpisodeCreate, db: Session = Depends(get_db)):
    """Creates episode for user"""
    new_ep = Episode(**episode.dict())
    db.add(new_ep)
    db.commit()
    db.refresh(new_ep)
    return {'message': "episode has been created"}


@router.get('/')
async def get_all(db: Session = Depends(get_db)):
    """Retrieves all episodes """
    ep_all = db.query(Episode).all()
    return ep_all


@router.get('/{_id}')
async def get_all(_id: int, db: Session = Depends(get_db)):
    """Retrives episodes by id """
    ep_get = db.query(Episode).filter(Episode.id == _id).first()
    if not ep_get:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail={'mess': f'episode with such id does not exists'})
    return {'episode_details': ep_get}


@router.put('/{_id}')
async def get_all(_id: int, serial: EpisodeCreate, db: Session = Depends(get_db)):
    """Update episode by id """
    ep_q = db.query(Episode).filter(Episode.id == _id)
    ep_put = ep_q.first()
    if not ep_put:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail={'mess': f'episode with such id does not exists'})
    ep_q.update(serial.dict(), synchronize_session=False)
    db.commit()
    return {'ser_det': ep_q.first()}


@router.delete('/{_id}')
async def get_all(_id: int, db: Session = Depends(get_db)):
    """Delete episode by id """
    ep_q = db.query(Episode).filter(Episode.id == _id)
    ep_del = ep_q.first()
    if not ep_del:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail={'mess': f'episode with such id does not exists'})
    ep_q.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
