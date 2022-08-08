import requests

class TestCookieMethod:
    def test_homework_cookie(self):
        url = "https://playground.learnqa.ru/api/homework_cookie"
        response = requests.get(url)
        assert response.status_code == 200, "Wrong response code"

        print(response.cookies)
        expected_cookie_value = "hw_value"
        actual_cookie_value = response.cookies.get("HomeWork")
        assert actual_cookie_value == expected_cookie_value, "Actual cookie value is not expected"
