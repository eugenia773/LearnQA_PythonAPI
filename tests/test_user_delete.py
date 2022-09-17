import requests
from lib.assertions import Assertions
from lib.base_case import BaseCase


class TestUserDelete(BaseCase):
    # Тест на удаление пользователя id = 2
    def test_delete_user_id2(self):
        # Login
        login_data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response1 = requests.post("https://playground.learnqa.ru/api/user/login", data=login_data)
        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id = self.get_json_value(response1, "user_id")

        Assertions.assert_code_status(response1, 200)

        # Delete
        response2 = requests.delete(
            f"https://playground.learnqa.ru/api/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_code_status(response2, 400)
        Assertions.assert_response_text(response2, "Please, do not delete test users with ID 1, 2, 3, 4 or 5.")

    # Тест на удаление только что созданного пользователя
    def test_delete_user_created(self):
        # Register
        register_data = self.prepare_registration_data()
        response1 = requests.post("https://playground.learnqa.ru/api/user/", data=register_data)

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
        response2 = requests.post("https://playground.learnqa.ru/api/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # Delete
        response3 = requests.delete(
            f"https://playground.learnqa.ru/api/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_code_status(response3, 200)

        # Get
        response4 = requests.get(
            f"https://playground.learnqa.ru/api/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
        )

        Assertions.assert_code_status(response4, 404)
        Assertions.assert_response_text(response4, "User not found")

    # Тест на удаление пользователя другим авторизованным пользователем
    def test_delete_user_from_another_user(self):
        # Register user 1
        register_data1 = self.prepare_registration_data()
        response1 = requests.post("https://playground.learnqa.ru/api/user/", data=register_data1)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email1 = register_data1['email']
        password1 = register_data1['password']

        # Register user 2
        register_data2 = self.prepare_registration_data()
        response2 = requests.post("https://playground.learnqa.ru/api/user/", data=register_data2)

        Assertions.assert_code_status(response2, 200)
        Assertions.assert_json_has_key(response2, "id")

        user2_id = self.get_json_value(response2, "id")

        # Login by user 1
        login_data1 = {
            'email': email1,
            'password': password1
        }
        response3 = requests.post("https://playground.learnqa.ru/api/user/login", data=login_data1)

        auth_sid1 = self.get_cookie(response3, "auth_sid")
        token1 = self.get_header(response3, "x-csrf-token")

        # Delete user 2 by user 1
        response4 = requests.delete(
            f"https://playground.learnqa.ru/api/user/{user2_id}",
            headers={"x-csrf-token": token1},
            cookies={"auth_sid": auth_sid1}
        )

        Assertions.assert_code_status(response4, 200)

        # Get
        response5 = requests.get(
            f"https://playground.learnqa.ru/api/user/{user2_id}",
            headers={"x-csrf-token": token1},
            cookies={"auth_sid": auth_sid1},
        )

        Assertions.assert_code_status(response5, 200)
        Assertions.assert_json_has_key(response5, "username")
