"""формированиен весов слов для словаря rusentilex"""
import csv
from itertools import zip_longest
import pandas as pd


def get_weights(tones):
    result = []
    for i in tones:
        if i == 'positive':
            result.append(1)
        else:
            result.append(-1)
    return result


df = pd.read_csv('D:\\GitHub\\sentiment-analyzer\\app\\dictionaries\\rusentilex.csv',
                 encoding='utf-8')
term = df['term'].tolist()
weight = get_weights(df['tone'].tolist())

d = [term, weight]
export_data = zip_longest(*d, fillvalue='')

with open('D:\\GitHub\\sentiment-analyzer\\app\\dictionaries\\rusentilex.csv', 'w',
          newline='', encoding='utf-8') as f:
    wr = csv.writer(f)
    wr.writerow(("term", "weight"))
    wr.writerows(export_data)
f.close()
