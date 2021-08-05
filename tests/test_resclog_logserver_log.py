import re
import os
import json
from fastapi.testclient import TestClient
from resc.resclog.logserver.log import *

client = TestClient(app)

def test_index():
    response = client.get("/")
    assert response.status_code == 200
    assert re.match(
        r'^text/html',
        response.headers["content-type"],
        flags=re.IGNORECASE,
    ) is not None

def test_css():
    response = client.get("/css/index.css")
    assert response.status_code == 200
    assert re.match(
        r'^text/css',
        response.headers["content-type"],
        flags=re.IGNORECASE,
    ) is not None

def test_js():
    response = client.get("/js/index-bundle.js")
    assert response.status_code == 200
    assert re.match(
        r'^application/javascript',
        response.headers["content-type"],
        flags=re.IGNORECASE,
    ) is not None

def test_analyze():
    test_file = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "test_data/output"
        )
    )
    response = client.post(
        "/analyze",
        files={
            "logfile": (
                "output",
                open(test_file,"rb"),
                "multipart/form-data"
            )
        },
    )
    content = json.loads(response.content)
    assert response.status_code == 200
    assert re.match(
        r'^application/json',
        response.headers["content-type"],
        flags=re.IGNORECASE,
    ) is not None
    assert content["result"] == "success"

def test_analyze_empty(logfile_empty):
    response = client.post(
        "/analyze",
        files={
            "logfile": (
                "output",
                open(logfile_empty,"rb"),
                "multipart/form-data"
            )
        },
    )
    assert response.status_code == 200
    assert re.match(
        r'^application/json',
        response.headers["content-type"],
        flags=re.IGNORECASE,
    ) is not None
    content = json.loads(response.content)
    assert content["result"] == "failure"
    assert re.match(
        r"^this is not resclog file.",
        content["explain"]
    ) is not None
