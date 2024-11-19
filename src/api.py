import os
import sys
import uuid
import time
import json
import pathlib
import contextlib

import uvicorn

import fastapi
from fastapi import HTTPException, Request, Security, Depends

from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.security.api_key import APIKey, APIKeyHeader
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.status import (
    HTTP_200_OK,
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR,
)

import docs
import config
import version
import auth_header

import utils


app = fastapi.FastAPI(
    title=config.API_TITLE,
    version=config.API_VERSION,
    openapi_tags=docs.ENDPOINT_TAGS,
    description=docs.DESCRIPTION,
    swagger_ui_parameters={
        "syntaxHighlight.theme": "obsidian",
        "defaultModelsExpandDepth": -1,
    },
    json_schema_extra=None,
)

app.add_middleware(GZipMiddleware, minimum_size=2000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@contextlib.asynccontextmanager
async def lifespan(app: fastapi.FastAPI):
    utils.log({"body": "API Service Started", "context": "startup_event"})
    yield
    utils.log({"body": "API Service Stopped", "context": "shutdown_event"})


@app.middleware("http")
async def add_context(request: Request, call_next):
    """Middleware that processes every request and response"""
    start_time = time.time()
    request.state.request_id = request.query_params.get("request_id", str(uuid.uuid4()))

    body = None
    if request.method == "POST":
        try:
            body = await request.json()
        except:
            pass

    headers_to_log = {
        k: v for k, v in request.headers.items() if k.lower() != "x-api-key"
    }

    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["x-process-time"] = f"{process_time:0.6f}"
    response.headers["request_id"] = request.state.request_id
    response.headers["api_version"] = version.__version__
    request_info = {
        "request_id": request.state.request_id,
        "method": request.method,
        "path": request.url.path,
        "status_code": response.status_code,
        "process_time": f"{process_time:0.6f}",
        "headers": headers_to_log,
        "json_payload": body,
    }
    utils.log(f"Request received:\n{json.dumps(request_info, indent=4)}")
    return response


@app.get("/assets/{filepath:path}", include_in_schema=False)
async def get_file(filepath: str):
    file_location = (
        pathlib.Path(__file__).parent.resolve().absolute().joinpath("assets") / filepath
    )
    if file_location.exists():
        return FileResponse(str(file_location))
    else:
        return JSONResponse(
            status_code=HTTP_404_NOT_FOUND,
            content={"message": "File not found", "file": filepath},
        )


@app.get("/health", tags=["API"])
def health():
    return JSONResponse(content={"status": "available"}, status_code=HTTP_200_OK)


@app.get("/ping", summary="Ping", tags=["API"])
async def ping(
    request: Request, api_key: APIKey = Depends(auth_header.validate_api_key)
):
    """
    Health check with API KEY

    Args:
        request (Request): HTTP request
        api_key (APIKey): API key

    Returns:
        HTTP JSON response
    """
    utils.log(f"Ping endpoint requested by {request.state.request_id}")
    message = {
        "id": request.state.request_id,
        "timestamp": str(utils.now()),
        "version": config.API_VERSION,
        "body": "Ping endpoint requested.",
        "metadata": {
            "request_id": str(request.state.request_id),
            "client_host": str(request.client.host),
            "request_headers": str(request.headers.raw),
        },
    }
    utils.log(message)
    return {"ping": "pong", "request_id": request.state.request_id}


from routers.example1 import example1_router

app.include_router(example1_router)

from routers.example2 import example2_router

app.include_router(example2_router)

from routers.web import web_router

app.include_router(web_router)


if __name__ == "__main__":
    import uvicorn

    utils.log("Starting directly...")
    try:
        uvicorn.run(
            "api:app",
            host="0.0.0.0",
            port=int(os.getenv("API_PORT", 8081)),
            reload=False,
            use_colors=True,
        )
    except Exception as e:
        error = json.dumps(utils.get_exception_details(), indent=4)
        utils.log(f"Error:\n{error}")
        sys.exit(1)
