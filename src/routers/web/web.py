import pathlib
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

import utils
import config
import auth_header
from lib import library


web_router = APIRouter(
    prefix="",
    tags=["Web"],
    responses={404: {"description": "Not found"}},
)


@web_router.get(
    "/", summary="Landing page", response_class=HTMLResponse, include_in_schema=False
)
async def index(request: Request):
    templates = Jinja2Templates(
        directory=str(pathlib.Path(config.BASE_DIR, "routers", "web", "templates"))
    )
    return templates.TemplateResponse("index.html", {"request": request})
