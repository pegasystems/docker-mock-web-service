import json
import unittest

import urllib3

import server

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


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
        response = self.app.get(server.PATH_HEADERS, headers={'Key': 'Value'})
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.get_data())
        self.assertEqual('Value', data['headers']['Key'])

    def test_redirect(self):
        response = self.app.get(server.PATH_REDIRECT,
                                headers={'X-Forwarded-Host': 'mylb', 'X-Forwarded-Proto': 'https'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual('https://mylb/', response.headers.get('Location'))

    def test_send_request(self):
        targetUrl = 'https://httpbin.org/get'
        response = self.app.post(server.PATH_REQUEST, json={server.TARGET_FIELD: targetUrl})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data())
        self.assertEqual(data[server.RESPONSECODE], 200)
        responseData = json.loads(data[server.DATA_FIELD])
        self.assertEqual(targetUrl, responseData['url'])

    def test_send_request_bad(self):
        targetUrl = 'https://192.168.88.99'
        response = self.app.post(server.PATH_REQUEST, json={server.TARGET_FIELD: targetUrl})
        data = json.loads(response.get_data())
        self.assertEqual(data[server.SUCCESS_FIELD], False)
        self.assertEqual(data[server.MESSAGE_FIELD], 'connection_error')

    def test_tcp_connection(self):
        response = self.app.post(server.PATH_TCP, json={server.TARGET_FIELD: '127.0.0.1', server.PORT_FIELD: 9999})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data())
        self.assertEqual(data[server.MESSAGE_FIELD], 'connection_refused')

    def test_postgres(self):
        response = self.app.post(server.PATH_POSTGRES,
                                 json={server.TARGET_FIELD: '127.0.0.1', server.USER_FIELD: "user",
                                       server.PASSWORD_FIELD: "password"})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data())
        self.assertEqual(data[server.SUCCESS_FIELD], False)

    def test_search_get(self):
        response = self.app.get(server.PATH_SEARCH)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data())
        self.assertEqual(data[server.RESPONSECODE], 200)

    def test_search_get_with_id(self):
        tenant_id = 'testid2616'
        response = self.app.get(server.PATH_SEARCH + tenant_id + '/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data())
        self.assertEqual(data[server.RESPONSECODE], 200)
        self.assertEqual(data["tenantID"], tenant_id)

    def test_search_post(self):
        tenant_id = 'testid2617'
        for path in ['model', 'index', 'query']:
            response = self.app.post(server.PATH_SEARCH + tenant_id + '/' + path)
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.get_data())
            self.assertEqual(data["Status"], "Ok")


if __name__ == "__main__":
    unittest.main()
