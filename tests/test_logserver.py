import unittest
from resc.resclog.logserver.server import start_server
from multiprocessing import Process
import time
import requests

class TestLogServer(unittest.TestCase):
	_IP="http://localhost:55555"
	def request(self):
		response = requests.get(self._IP)
		return response.status_code
	def test_server(self):
		process = Process(target=start_server,daemon=False)
		process.start()
		time.sleep(5)
		status_code = self.request()
		process.kill()

		self.assertIsNotNone(status_code)
		self.assertEqual(200,status_code)

if __name__ == "__main__":
	unittest.main()
