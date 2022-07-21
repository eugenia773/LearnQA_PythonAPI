import json

json_text = '{"messages":[{"message":"This is the first message","timestamp":"2021-06-04 16:40:53"},' \
            '{"message":"And this is a second message","timestamp":"2021-06-04 16:41:01"}]}'
obj = json.loads(json_text)

key1 = "messages"
key2 = "message"

if key1 in obj:
    if key2 in obj[key1][1]:
        print(obj[key1][1][key2])
    else:
        print(f"Ключа {key2} нет в JSON")
else:
    print(f"Ключа {key1} нет в JSON")
