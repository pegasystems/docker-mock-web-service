import unittest
import json
import server

class TestMockServer(unittest.TestCase):
    
    def setUp(self):
        self.app = server.app.test_client()
        self.app.testing = True

    def test_root(self):
        response = self.app.get(server.PATH_ROOT)
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data[server.MESSAGE_FIELD], server.DEFAULT_MESSAGE)

    def test_delay(self):
        response = self.app.get(server.PATH_DELAY + "?" + server.SECONDS + "=1")
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data[server.SECONDS], 1)
    
    def test_echo(self):
        response = self.app.post(server.PATH_ECHO + "?" + server.MESSAGE_FIELD + "=hi")
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data[server.MESSAGE_FIELD], "hi")
        self.assertEqual(data[server.METHOD], "POST")

    def test_code(self):
        response = self.app.get(server.PATH_CODE + "?" + server.RESPONSECODE + "=402")
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 402)
        self.assertEqual(data[server.RESPONSECODE], 402)
        
    def test_count(self):
        response = self.app.get(server.PATH_COUNT)
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data[server.COUNT], 1)

        response = self.app.get(server.PATH_COUNT)
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data[server.COUNT], 2)

        response = self.app.get(server.PATH_COUNT)
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data[server.COUNT], 3)

if __name__ == "__main__":
    unittest.main()