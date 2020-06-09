import json

with open('D:\\GitHub\\sentiment-analyzer\\app\static\\reviews.json', 'r', encoding='utf-8') as f:
    js = json.load(f)

for j in js:
    for i in j:
        print(i['rating'])
