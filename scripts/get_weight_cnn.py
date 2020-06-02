# загружаем неразмеченный словарь из json файла
import csv
import json
from itertools import zip_longest

import pandas as pd
import numpy as np

""" 
Get new csv file with term, frequency, tone for next operations
with open('unallocated_dictionary.json', 'r', encoding='utf-8') as f:
    js = json.load(f)

unallocated_words = [word[0] for word in js]
unallocated_frequency = [word[1] for word in js]

df = pd.read_csv('D:\\GitHub\\sentiment-analyzer\\app\\dictionaries\\original\\dict_cnn.csv', encoding='utf-8')
tone = df['tone'].tolist()

d = [unallocated_words, unallocated_frequency, tone]
export_data = zip_longest(*d, fillvalue='')

with open('D:\\GitHub\\sentiment-analyzer\\scripts\\cnn_dict_tmp.csv', 'w', encoding='utf-8',
          newline='') as f:
    wr = csv.writer(f)
    wr.writerow(("term", "frequency", "tone"))
    wr.writerows(export_data)
f.close()
"""


def scale_positive(chi_square):
    return 1 * (chi_square - np.min(chi_square)) / (np.max(chi_square) - np.min(chi_square))


def scale_negative(chi_square):
    return -1 * (chi_square - np.min(chi_square)) / (np.max(chi_square) - np.min(chi_square))


df = pd.read_csv('D:\\GitHub\\sentiment-analyzer\\scripts\\cnn_dict_tmp.csv', encoding='utf-8')

tone = df['tone'].tolist()
term = df['term'].tolist()
frequency = df['frequency'].tolist()

positive_tone = []
positive_term = []
positive_f = []

negative_term = []
negative_f = []

for i in range(0, len(tone)):
    if tone[i] == 'positive':
        positive_term.append(term[i])
        positive_f.append(frequency[i])
    else:
        negative_term.append(term[i])
        negative_f.append(frequency[i])

negative = np.array(negative_f)
negative_scaled = scale_negative(negative)

positive = np.array(positive_f)
positive_scaled = scale_positive(positive)

scale = list(positive_scaled) + list(negative_scaled)

d = [positive_term + negative_term, scale]
export_data = zip_longest(*d, fillvalue='')

with open('D:\\GitHub\\sentiment-analyzer\\app\\dictionaries\\cnn_dict.csv', 'w', encoding='utf-8',
          newline='') as f:
    wr = csv.writer(f)
    wr.writerow(("term", "weight"))
    wr.writerows(export_data)
f.close()
