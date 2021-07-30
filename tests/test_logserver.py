from resc.resclog.logserver.server import start_server
from multiprocessing import Process
import time
import requests
import pytest
import asyncio

_IP="http://localhost:5555"
class TestServer:
	def setup_server(self):
		self.process = Process(target=start_server,daemon=False)
		self.process.start()
	def terminate_server(self):
		self.process.kill()

@pytest.fixture(scope="module",autouse=True)
def setup_server():
	server = TestServer()
	server.setup_server()
	time.sleep(5)
	yield server
	server.terminate_server()

def test_index(setup_server):
	server = setup_server

	response = requests.get(_IP,timeout=30)
	assert response is not None
	assert isinstance(response.status_code,int)
	assert response.status_code == 200
	assert isinstance(response.content,bytes)
	assert len(response.content)>0

	print(response.content)
