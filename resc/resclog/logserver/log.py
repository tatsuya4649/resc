import os
from fastapi import FastAPI, File, UploadFile
from fastapi.staticfiles import StaticFiles
from ..analyze import RescLogAnalyze


app = FastAPI()


@app.post("/analyze")
async def analyze(logfile: UploadFile = File(...)):
    log = await logfile.read()
    analyze = RescLogAnalyze.analyze(log)
    if len(analyze) == 0:
        return {"result": "failure", "explain": "this is not resclog file."}
    return {"result": "success", "analyze": analyze}


app.mount(
    "/js",
    StaticFiles(
        directory=f"{os.path.dirname(__file__)}/static/public/js",
        html=False),
    name="js"
)
app.mount(
    "/css",
    StaticFiles(
        directory=f"{os.path.dirname(__file__)}/static/public/css",
        html=False),
    name="css"
)
app.mount(
    "/",
    StaticFiles(
        directory=f"{os.path.dirname(__file__)}/static/public/html",
        html=True),
    name="html",
)
