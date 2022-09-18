import allure
import time
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions


@allure.epic("Edit user cases")
class TestUserEdit(BaseCase):
    @allure.description("This test checks just created user can be edited")
    @allure.severity(severity_level="Critical")
    @allure.tag("Smoke")
    def test_edit_just_created_user(self):
        # Register
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(response1, "id")

        # Login
        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # Edit
        new_name = "Changed Name"
        response3 = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_name}
        )

        Assertions.assert_code_status(response3, 200)

        # Get
        response4 = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
        )

        Assertions.assert_json_value_by_name(
            response4,
            "firstName",
            new_name,
            "Wrong name of the user after edit"
        )

    # Тест на изменение данных (fisrtName) пользователя неавторизованным пользователем
    @allure.description("This test checks user data can't be edited from unauthorized user")
    @allure.severity(severity_level="Critical")
    @allure.tag("Smoke")
    def test_edit_user_from_not_auth(self):
        # Register
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        user_id = self.get_json_value(response1, "id")

        # Edit from not auth user
        new_name = "Changed Name"
        response2 = MyRequests.put(
            f"/user/{user_id}",
            data={"firstName": new_name}
        )

        Assertions.assert_code_status(response2, 400)
        Assertions.assert_response_text(response2, "Auth token not supplied")

    # Тест на изменение данных (firstName) пользователя другим авторизованным пользователем
    @allure.description("This test checks user data can't be edited from another authorized user")
    @allure.severity(severity_level="Critical")
    @allure.tag("Smoke")
    def test_edit_user_from_another_auth_user(self):
        # Register user 1
        register_data1 = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data1)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email1 = register_data1['email']
        password1 = register_data1['password']

        time.sleep(1)

        # Register user 2
        register_data2 = self.prepare_registration_data()
        response2 = MyRequests.post("/user/", data=register_data2)

        Assertions.assert_code_status(response2, 200)
        Assertions.assert_json_has_key(response2, "id")

        email2 = register_data2['email']
        password2 = register_data2['password']
        first_name2 = register_data2['firstName']
        user2_id = self.get_json_value(response2, "id")

        # Login by user 1
        login_data1 = {
            'email': email1,
            'password': password1
        }
        response3 = MyRequests.post("/user/login", data=login_data1)

        auth_sid1 = self.get_cookie(response3, "auth_sid")
        token1 = self.get_header(response3, "x-csrf-token")

        # Edit user 2 from user 1
        new_name = "Changed Name"
        response4 = MyRequests.put(
            f"/user/{user2_id}",
            headers={"x-csrf-token": token1},
            cookies={"auth_sid": auth_sid1},
            data={"firstName": new_name}
        )

        Assertions.assert_code_status(response4, 200)

        # Login by user 2 and check new name
        login_data2 = {
            'email': email2,
            'password': password2
        }
        response5 = MyRequests.post("/user/login", data=login_data2)

        auth_sid2 = self.get_cookie(response5, "auth_sid")
        token2 = self.get_header(response5, "x-csrf-token")

        response6 = MyRequests.get(
            f"/user/{user2_id}",
            headers={"x-csrf-token": token2},
            cookies={"auth_sid": auth_sid2},
        )

        actual_name = response6.json()["firstName"]
        expected_name = first_name2
        Assertions.assert_code_status(response6, 200)
        Assertions.assert_json_value_by_name(response6, "firstName", expected_name,
                                             f"Wrong user name. Expected: {expected_name}, Actual: {actual_name}")

    # Тест на изменение email пользователя (email не валиден - без @)
    @allure.description("This test checks new email can't be invalid - without @ symbol")
    @allure.severity(severity_level="Normal")
    def test_edit_user_wrong_email(self):
        # Register
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        password = register_data['password']
        user_id = self.get_json_value(response1, "id")

        # Login
        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # Edit
        new_email = "testuseremailexample.com"
        response3 = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"email": new_email}
        )

        Assertions.assert_code_status(response3, 400)
        Assertions.assert_response_text(response3, "Invalid email format")

    # Тест на изменение имени (firstName) пользователя (имя не валидно - 1 символ)
    @allure.description("This test checks new firstName user can't contain the only symbol")
    @allure.severity(severity_level="Minor")
    def test_edit_user_short_name(self):
        # Register
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        password = register_data['password']
        user_id = self.get_json_value(response1, "id")

        # Login
        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # Edit
        new_first_name = "q"
        response3 = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_first_name}
        )

        Assertions.assert_code_status(response3, 400)
        Assertions.assert_response_text(response3, '{"error":"Too short value for field firstName"}')
