import requests

# Запросы без параметра method
response_get = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type")
print("GET запрос без параметра method:", response_get.text)
response_post = requests.post("https://playground.learnqa.ru/ajax/api/compare_query_type")
print("POST запрос без параметра method:", response_post.text)
response_put = requests.put("https://playground.learnqa.ru/ajax/api/compare_query_type")
print("PUT запрос без параметра method:", response_put.text)
response_delete = requests.delete("https://playground.learnqa.ru/ajax/api/compare_query_type")
print("DELETE запрос без параметра method:", response_delete.text)
print("")

# Запрос не из списка (OPTIONS)
response2 = requests.options("https://playground.learnqa.ru/ajax/api/compare_query_type")
print(response2.text)
print("")

# Запрос с правильным значением method (здесь - только GET)
response3 = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type", params={"method": "GET"})
print(response3.text)
print("")

# Все возможные сочетания типов запроса и значений параметра method
method = {"GET", "POST", "PUT", "DELETE"}

for i in method:
    response_get = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type", params={"method": i})
    print("Метод:", i, "GET запрос:", response_get.text)

    response_post = requests.post("https://playground.learnqa.ru/ajax/api/compare_query_type", data={"method": i})
    print("Метод:", i, "POST запрос:", response_post.text)

    response_put = requests.put("https://playground.learnqa.ru/ajax/api/compare_query_type", data={"method": i})
    print("Метод:", i, "PUT запрос:", response_put.text)

    response_delete = requests.delete("https://playground.learnqa.ru/ajax/api/compare_query_type", data={"method": i})
    print("Метод:", i, "DELETE запрос:", response_delete.text)
