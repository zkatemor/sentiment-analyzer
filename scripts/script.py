import json

import pandas as pd

with open('D:\\GitHub\\sentiment-analyzer\\app\static\\reviews.json', 'r', encoding='utf-8') as f:
    js = json.load(f)

texts = []
ratings = []

for model in js:
    for review in model:
        texts.append(str(review['pluses']) + '\n' + str(review['minuses']) + '\n' + str(review['comment']))
        ratings.append(review['rating'])

df = pd.DataFrame()
df['Text'] = texts
df['Rating'] = ratings

df.to_excel('D:\\GitHub\\sentiment-analyzer\\app\\static\\reviews.xlsx', index=False)
