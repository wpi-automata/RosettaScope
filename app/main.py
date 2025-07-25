from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .src.routers import stream_api
from .src.StreamManager import StreamManager
from .src.ParserManager import ParserManager
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import contextlib

stream_manager = StreamManager()
parser_manager = ParserManager(stream_manager)
app = FastAPI()

app.include_router(stream_manager.router)
app.include_router(parser_manager.router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)