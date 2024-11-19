from fastapi import APIRouter, Query, Depends, File, UploadFile

import utils
import auth_header
from lib import library
from . import schemas


example1_router = APIRouter(
    prefix="/v1/example1",
    tags=["Examples"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(auth_header.validate_api_key)],
)


@example1_router.post("/voice-to-text", summary="Converts voice to text")
async def voice_to_text(audio: UploadFile = File(...)):
    utils.log(f"Content type: {audio.content_type}")
    return {"message": "Voice to text conversion is not yet implemented."}
