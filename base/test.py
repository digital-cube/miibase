from tornado.testing import AsyncHTTPTestCase

from base import http_exceptions as http

import json
import time

class TestBase(AsyncHTTPTestCase):

    def api(self, token, method, route, body=None,
            expected_code=(http.status.OK, http.status.CREATED, http.status.NO_CONTENT),
            expected_result=None,
            expected_result_subset=None,
            expected_result_contain_keys=None,
            expected_length=None,
            expected_lenght_for_key: tuple = None,
            raw_response=False,
            headers={},
            default_timeout=600):

        if not body:
            if method in ('PUT', 'POST', 'PATCH'):
                body = {}

        if method in ('GET', 'DELETE'):
            body = None

        headers.update({'Authorization': token} if token else {})
        stime = time.time()

        try:
            response = self.fetch(route,
                                  method=method,
                                  body=json.dumps(body, ensure_ascii=False) \
                                      if body is not None else None,
                                  headers=headers,
                                  connect_timeout=default_timeout,
                                  request_timeout=default_timeout)
        except Exception as e:
            self.assertTrue(False)

        self.execution_time = time.time() - stime
        self.last_result_code = response.code
        self.last_uri = f'{method} : {route}'
        if expected_code:
            if type(expected_code) == tuple:
                self.assertIn(response.code, expected_code)
            else:
                self.assertEqual(expected_code, response.code, msg=response.body)

        if raw_response:
            return response.body

        resp_txt = response.body.decode('utf-8')

        try:
            res = json.loads(resp_txt) if resp_txt else {}
            self.last_result = res
        except:
            self.assertTrue(False, 'Error decoding JSON')

        if expected_result:
            self.assertEqual(expected_result, res)

        if expected_result_contain_keys:
            for key in expected_result_contain_keys:
                self.assertTrue(key in res)

        if expected_result_subset:
            for key in expected_result_subset:
                self.assertTrue(key in res)
                self.assertEqual(expected_result_subset[key], res[key])

        if expected_length is not None:
            self.assertEqual(expected_length, len(res))

        if expected_lenght_for_key is not None:
            self.assertTrue(len(res[expected_lenght_for_key[0]]) == expected_lenght_for_key[1])

        self.last_result = res
        self.execution_time = time.time() - stime

        return res

    def show_last_result(self, marker='LAST_RES', indent=1):
        if hasattr(self, 'last_uri'):
            print(f"{marker} :: URI", self.last_uri)
        if hasattr(self, 'last_result_code'):
            print(f"{marker} :: code =", self.last_result_code, "EXECUTE TIME", round(self.execution_time, 4))
        if hasattr(self, 'last_result'):
            print(f"{marker} :: Last result content")
            print(json.dumps(self.last_result, indent=indent, ensure_ascii=False))
