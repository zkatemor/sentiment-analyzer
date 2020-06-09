import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

url = "https://market-scanner.ru/api/reviews"
key = os.environ.get('key')
reviews = []


def getReviewById(id):
    data = {'key': key,
            'id': id,
            }

    response = requests.post(url=url, data=data)

    js = response.json().get('reviews')
    print(js)
    reviews.append(js)


# 1) леново 201 2) леново 438 3) сяоми 629 4) хонор 421 5) мейзу 330 = 2019
ids = [9323494, 10414225, 13527763, 12423732, 12748971]

for i in ids:
    getReviewById(i)

with open('D:\\GitHub\\sentiment-analyzer\\app\\static\\reviews.json', 'w', encoding='utf-8') as f:
    json.dump(reviews, f, ensure_ascii=False, indent=4)
