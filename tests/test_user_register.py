import string
import pytest
import random
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
from datetime import datetime


class TestUserRegister(BaseCase):
    exclude_params = [
        "username",
        "firstName",
        "lastName",
        "email",
        "password"
    ]

    len_username = [
        "symbol_1",
        "symbol_251"
    ]

    def setup(self):
        base_part = "learnqa"
        domain = "example.com"
        random_part = datetime.now().strftime("%m%d%Y%H%M%S")
        self.email = f"{base_part}{random_part}@{domain}"

    def test_create_user_successfully(self):
        data = self.prepare_registration_data()
        response = MyRequests.post("/user/", data=data)
        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email)
        response = MyRequests.post("/user/", data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", \
            f"Unexpected response content {response.content}"

    def test_create_user_with_invalid_email(self):
        base_part = "learnqa"
        domain = "example.com"
        random_part = datetime.now().strftime("%m%d%Y%H%M%S")
        email = f"{base_part}{random_part}{domain}"

        data = {
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': email,
            'password': '123'
        }

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == "Invalid email format", \
            f"Unexpected response content {response.content}"

    @pytest.mark.parametrize('condition', exclude_params)
    def test_create_user_without_one_field(self, condition):
        if condition == "username":
            data = {
                'firstName': 'learnqa',
                'lastName': 'learnqa',
                'email': self.email,
                'password': '123'
            }
        elif condition == "firstName":
            data = {
                'username': 'learnqa',
                'lastName': 'learnqa',
                'email': self.email,
                'password': '123'
            }
        elif condition == "lastName":
            data = {
                'username': 'learnqa',
                'firstName': 'learnqa',
                'email': self.email,
                'password': '123'
            }
        elif condition == "email":
            data = {
                'username': 'learnqa',
                'firstName': 'learnqa',
                'lastName': 'learnqa',
                'password': '123'
            }
        elif condition == "password":
            data = {
                'username': 'learnqa',
                'firstName': 'learnqa',
                'lastName': 'learnqa',
                'email': self.email,

            }
        else:
            return

        response = MyRequests.post("/user/", data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The following required params are missed: {condition}", \
            f"Unexpected response content {response.content}"

    @pytest.mark.parametrize('condition', len_username)
    def test_create_user_with_wrong_size_username(self, condition):
        if condition == "symbol_1":
            len_uname = 1
            result = "short"
        elif condition == "symbol_251":
            len_uname = 251
            result = "long"
        else:
            return

        username = ''.join(random.choice(string.ascii_lowercase) for i in range(len_uname))
        data = {
            'username': username,
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': self.email,
            'password': '123'
        }

        response = MyRequests.post("/user/", data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The value of 'username' field is too {result}", \
            f"Unexpected response content {response.content}"
