from resc.resclog.logserver.server import start_server
from multiprocessing import Process
import time
import requests
import pytest
import asyncio

_IP="https://google.com"
class TestServer:
	async def setup_server(self):
		self.process = Process(target=start_server,daemon=True)
		self.process.start()
	async def terminate_server(self):
		self.process.terminate()

@pytest.fixture(scope="module",autouse=True)
async def setup_server():
	server = TestServer()
	await server.setup_server()
	await asyncio.sleep(10)
	yield
	await server.terminate_server()

def request():
	response = requests.get(_IP,timeout=30)
	return response

def test_index(setup_server):
	response = request()
	assert response.status_code == 200
	assert isinstance(response.content,bytes)

	print(response.content)
