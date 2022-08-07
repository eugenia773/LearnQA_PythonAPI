import requests

class TestHeaderMethod:
    def test_homework_header(self):
        url = "https://playground.learnqa.ru/api/homework_header"
        response = requests.get(url)
        assert response.status_code == 200, "Wrong response code"

        print(response.headers)
        expected_header_value = "Some secret value"
        actual_header_value = response.headers.get("x-secret-homework-header")
        assert actual_header_value == expected_header_value, "Actual header value is not expected"
