from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .src.routers import stream_api
from .src.StreamManager import StreamManager
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import contextlib

stream_manager = StreamManager()
app = FastAPI()

app.include_router(stream_manager.router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)