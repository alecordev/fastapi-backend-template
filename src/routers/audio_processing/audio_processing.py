import pathlib
from fastapi import APIRouter, Request, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

import utils
import config
import auth_header
from lib import library


audio_processing = APIRouter(
    prefix="",
    tags=["Web"],
    responses={404: {"description": "Not found"}},
)

templates = Jinja2Templates(
    directory=str(
        pathlib.Path(config.BASE_DIR, "routers", "audio_processing", "templates")
    )
)


@audio_processing.get("/audio", response_class=HTMLResponse, include_in_schema=False)
async def audio_processing(request: Request):
    return templates.TemplateResponse("audio-processing.html", {"request": request})


@audio_processing.post("/api/upload-audio")
async def upload_audio(audio: UploadFile = File(...)):
    contents = await audio.read()
    filename = audio.filename if audio.filename else "audio.wav"
    # return genai.save_and_transcribe_audio_locally(contents, filename)
