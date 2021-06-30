from tornado.testing import AsyncHTTPTestCase
import base.http_exceptions as http
import base.app

from base.test import TestBase


class TestRoutesApp(TestBase):
    def get_app(self):

        import app

        return base.app.make_app(print_routes=False)

    def test_no_param_route_get(self):
        self.api('token', 'GET', '/no-param-route', expected_code=http.status.OK, expected_result={'method': 'get'})

    def test_no_param_route_post(self):
        self.api('token', 'POST', '/no-param-route', expected_code=http.status.OK, expected_result={'method': 'post'})

    def test_no_param_route_patch(self):
        self.api('token', 'PATCH', '/no-param-route', expected_code=http.status.OK, expected_result={'method': 'patch'})

    def test_no_param_route_delete(self):
        self.api('token', 'DELETE', '/no-param-route', expected_code=http.status.OK,
                 expected_result={'method': 'delete'})

    # def test_fetch_non_existing_route(self):
    #     self.api('token', 'GET', '/non-existing-route', expected_code=None)
    #     self.show_last_result()

    def atest_int_param_route_get(self):
        self.api('token', 'GET', '/int-param-route?i_param=42', expected_code=http.status.OK,
                 expected_result={"method": "get", "type": "int", "value": 42})

    '''
    Invalid type for param type, int is expected
    Invalid type for param i_param, int is expected
    
    '''

    def test_int_param_route_get_provide_string_and_expect_error(self):
        self.api('token', 'GET', '/int-param-route?i_param=ABC', expected_code=http.status.BAD_REQUEST,
                 expected_result_subset={"id": "INVALID_PARAM",
                                         "message": "Invalid type for param ABC, int is expected",
                                         "code": http.status.BAD_REQUEST})

    def test_int_param_route_get_avoid_mandatory_argument_and_expect_error(self):
        self.api('token', 'GET', '/int-param-route', expected_code=http.status.BAD_REQUEST,
                 expected_result_subset={"id": "MISSING_PARAM",
                                         "message": "Mandatory argument i_param is not provided",
                                         "code": http.status.BAD_REQUEST})

    def test_int_param_route_get_avoid_optional_argument_and_expect_default_value_42(self):
        self.api('token', 'GET', '/optional-int-param-route', expected_code=http.status.OK)

    def test_int_param_route_post(self):
        self.api('token', 'POST', '/int-param-route', body={'i_param': 42},
                 expected_code=http.status.OK,
                 expected_result={"method": "post", "type": "int", "value": 42})

    def test_int_param_route_post_send_float_number_instead_int(self):
        self.api('token', 'POST', '/int-param-route', body={'i_param': 42.2},
                 expected_code=http.status.OK,
                 expected_result={"method": "post", "type": "int", "value": 42})

    def test_float_param_route_get(self):
        self.api('token', 'GET', '/float-param-route?f_param=3.14159', expected_code=http.status.OK,
                 expected_result={"method": "get", "type": "float", "value": 3.14159})

    def test_list_param_in_post(self):
        self.api('token', 'POST', '/list-param-route', body={'l_param': [1, 2, 3, '4', 'pet']},
                 expected_code=http.status.OK)
        self.show_last_result()