import unittest
from resc.resclog.logserver.server import start_server

class TestLogServer(unittest.TestCase):
	def test_server(self):
		start_server()
