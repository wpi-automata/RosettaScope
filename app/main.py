from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .src.routers import stream_api
from .src.StreamManager import StreamManager

app = FastAPI()

app.mount('/home', StaticFiles(directory='static', html=True), name='static')

stream_manager = StreamManager()
app.include_router(stream_manager.router)
