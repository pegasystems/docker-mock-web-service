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

    def test_health_check(self):
        response = self.app.get(server.PATH_HEALTH)
        self.assertEqual(response.status_code, 200)

        response = self.app.get(server.PATH_SET_HEALTH + "?" + server.RESPONSECODE + "=500")
        self.assertEqual(response.status_code, 200)

        response = self.app.get(server.PATH_HEALTH)
        self.assertEqual(response.status_code, 500)

        response = self.app.get(server.PATH_SET_HEALTH + "?" + server.RESPONSECODE + "=200")
        self.assertEqual(response.status_code, 200)

        response = self.app.get(server.PATH_HEALTH)
        self.assertEqual(response.status_code, 200)

    def test_headers(self):
        response = self.app.get(server.PATH_HEADERS, headers={'Key' : 'Value'})
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.get_data())
        self.assertEqual('Value', data['headers']['Key'])

    def test_redirect(self):
        response = self.app.get(server.PATH_REDIRECT, headers={'X-Forwarded-Host' : 'mylb', 'X-Forwarded-Proto' : 'https'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual('https://mylb/', response.headers.get('Location'))

if __name__ == "__main__":
    unittest.main()