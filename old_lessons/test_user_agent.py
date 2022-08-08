import json
import pytest
import requests


class TestUserAgent:
    user_agent_data = [
        {
            "user-agent": "Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) AppleWebKit/534.30 "
                          "(KHTML, like Gecko) Version/4.0 Mobile Safari/534.30",
            "platform": "Mobile",
            "browser": "No",
            "device": "Android"
        },
        {
            "user-agent": "Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) "
                          "CriOS/91.0.4472.77 Mobile/15E148 Safari/604.1",
            "platform": "Mobile",
            "browser": "Chrome",
            "device": "iOS"
        },
        {
            "user-agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
            "platform": "Googlebot",
            "browser": "Unknown",
            "device": "Unknown"
        },
        {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.100.0",
            "platform": "Web",
            "browser": "Chrome",
            "device": "No"
        },
        {
            "user-agent": "Mozilla/5.0 (iPad; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, "
                          "like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
            "platform": "Mobile",
            "browser": "No",
            "device": "iPhone"
        }
    ]

    @pytest.mark.parametrize("user_agent", user_agent_data)
    def test_user_agent(self, user_agent):
        url = "https://playground.learnqa.ru/ajax/api/user_agent_check"
        data = {"user-agent": user_agent["user-agent"]}
        response = requests.get(url, headers=data)
        assert response.status_code == 200, "Wrong response code"

        assert user_agent["platform"] == json.loads(response.text)["platform"], f"Value for 'platform' is not equal to '{user_agent['platform']}' for User-Agent '{user_agent['user-agent']} "
        assert user_agent["browser"] == json.loads(response.text)["browser"], f"Value for 'browser' is not equal to '{user_agent['browser']}' for User-Agent '{user_agent['user-agent']} "
        assert user_agent["device"] == json.loads(response.text)["device"], f"Value for 'device' is not equal to '{user_agent['device']}' for User-Agent '{user_agent['user-agent']} "
