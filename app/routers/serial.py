from fastapi import APIRouter, status, Response, Depends, Form, File, HTTPException, UploadFile
from sqlalchemy.orm import Session
from shutil import copy

from .. import schemas, models
from ..db import get_db

import uuid


router = APIRouter(
    prefix="/serial",
    tags=['serial']
)


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_serial(name: str = Form(...), description: str = Form(...), owner_id: int = Form(...), file: UploadFile = File(...), db: Session = Depends(get_db)):
    """Creates serial for user"""
    path = 'upload_files/'
    file.filename = f'{name}{file.filename[file.filename.rindex("."):]}'
    with open(file.filename, 'wb') as f:
        copy(file.filename, path)
    serialize = schemas.SerialS(name=name, description=description, owner_id=owner_id)
    new_ser = models.Serial(name=serialize.name, description=serialize.description, photo_path=path + file.filename, owner_id=serialize.owner_id)
    db.add(new_ser)
    db.commit()
    #db.refresh(new_ser)
    return {'message': "serial has been created"}


@router.get('/')
async def get_all(db: Session = Depends(get_db)):
    """Retrieves all serials """
    ser_all = db.query(models.Serial).all()
    return ser_all


@router.get('/{_id}')
async def get_all(_id: int, db: Session = Depends(get_db)):
    """Retrives serials by id """
    ser_get = db.query(models.Serial).filter(models.Serial.id == _id).first()
    if not ser_get:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail={'mess': f'post with such id does not exists'})
    return {'ser_det': ser_get}


@router.put('/{_id}')
async def get_all(_id: int, serial: schemas.SerialS, db: Session = Depends(get_db)):
    """Update serial by id """
    ser_q = db.query(models.Serial).filter(models.Serial.id == _id)
    ser_put = ser_q.first()
    if not ser_put:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail={'mess': f'post with such id does not exists'})
    ser_q.update(serial.dict(), synchronize_session=False)
    db.commit()
    return {'ser_det': ser_q.first()}


@router.delete('/{_id}')
async def get_all(_id: int, db: Session = Depends(get_db)):
    """Delete serial by id """
    ser_q = db.query(models.Serial).filter(models.Serial.id == _id)
    ser_del = ser_q.first()
    if not ser_del:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail={'mess': f'post with such id does not exists'})
    ser_q.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
