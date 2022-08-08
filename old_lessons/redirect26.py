import requests

response = requests.get("https://playground.learnqa.ru/api/long_redirect", allow_redirects=True)

redirect_count = len(response.history)
print("Number of redirects =", redirect_count)
print("Result URL:", response.url)
