from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()
app.mount("/js",StaticFiles(directory=f"{os.path.dirname(__file__)}/static/public/js",html=False),name="js")
app.mount("/",StaticFiles(directory=f"{os.path.dirname(__file__)}/static/public/html",html=True),name="html")
