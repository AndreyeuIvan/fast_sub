from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse

from app.routers import user, episode, serial

from shutil import copy


app = FastAPI()

app.include_router(user.router)
app.include_router(episode.router)
app.include_router(serial.router)


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    with open(file.filename, 'wb') as f:
        copy(file.filename, 'app/upload_files/')
    return {"filename": file.filename}


@app.post("/download/")
async def create_upload_file():
    return FileResponse('app/upload_files/')
