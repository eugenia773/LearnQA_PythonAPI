import requests
import time
import json
from json.decoder import JSONDecodeError

response1 = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job")

try:
    token = response1.json()["token"]
    sec = response1.json()["seconds"]
except JSONDecodeError:
    print("Response is not a JSON format")
    token = ""
    sec = ""

response2 = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job", params={"token": token})

status_not_ready = "Job is NOT ready"
status_ready = "Job is ready"
key_res = "result"

try:
    status_current = response2.json()["status"]
except JSONDecodeError:
    print("Response is not a JSON format")
    status_current = ""

if status_current == status_not_ready:
    print("Status is correct: Job is NOT ready")
    time.sleep(sec)

    response3 = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job", params={"token": token})

    try:
        status_current = response3.json()["status"]
    except JSONDecodeError:
        print("Response is not a JSON format")
        status_current = ""

    obj = json.loads(response3.text)
    if (status_current == status_ready) and (key_res in obj):
        print("Status is correct and result is in response")
        print("Result =", obj[key_res])
    else:
        print("Status is incorrect or/and result is not in response")
else:
    print("Status is incorrect")
