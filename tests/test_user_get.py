import allure
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions


@allure.epic("Get user cases")
class TestUserGet(BaseCase):
    @allure.description("This test checks not authorized user can get only username")
    @allure.severity(severity_level="Critical")
    @allure.tag("Smoke")
    def test_get_user_details_not_auth(self):
        response = MyRequests.get("/user/2")

        Assertions.assert_json_has_key(response, "username")
        Assertions.assert_json_has_not_key(response, "email")
        Assertions.assert_json_has_not_key(response, "firstName")
        Assertions.assert_json_has_not_key(response, "lastName")

    @allure.description("This test checks authorized user can get all his fields")
    @allure.severity(severity_level="Critical")
    @allure.tag("Smoke")
    def test_get_user_details_auth_as_same_user(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response1 = MyRequests.post("/user/login", data=data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(response1, "user_id")

        response2 = MyRequests.get(
            f"/user/{user_id_from_auth_method}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        expected_fields = ["username", "email", "firstName", "lastName"]
        Assertions.assert_json_has_keys(response2, expected_fields)

    @allure.description("This test checks authorized user can get only username from another user data")
    @allure.severity(severity_level="Critical")
    @allure.tag("Smoke")
    def test_get_user_details_auth_as_another_user(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response1 = MyRequests.post("/user/login", data=data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")

        response2 = MyRequests.get(
            "/user/1",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        unexpected_keys = ["email", "firstName", "lastName"]
        Assertions.assert_code_status(response2, 200)
        Assertions.assert_json_has_key(response2, "username")
        Assertions.assert_json_has_not_keys(response2, unexpected_keys)
