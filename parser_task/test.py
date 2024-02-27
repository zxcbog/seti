import requests
import json

response = requests.post("http://127.0.0.1:8080", json={'url':"https://www.muztorg.ru/category/akusticheskie-gitary"})
data = json.loads(response.text[:-1])
with open("data_from_api.csv", "w") as f:
    for foreign_key in data.keys():
        item = data[foreign_key]
        item_keys_len = len(item.keys())
        for i, key in enumerate(item.keys()):
            f.write(f"{item[key]}")
            if i != item_keys_len - 1:
                f.write(";")
        f.write("\n")