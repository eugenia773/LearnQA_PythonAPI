import requests

response = requests.get("https://playground.learnqa.ru/api/long_redirect", allow_redirects=True)

resp = response.history
elem = len(resp)

print("Number of redirects =", elem - 1)
print("Result URL:", resp[elem - 1].url)
