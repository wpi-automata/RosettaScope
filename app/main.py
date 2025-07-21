# import flask

# app = flask.Flask(__name__)

# @app.route('/')
# def home():
#     return flask.render_template('index.html')
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount('/', StaticFiles(directory='static', html=True), name='static')

# @app.get('/')
# async def root():
#     return StaticFiles.file_response('index.html')