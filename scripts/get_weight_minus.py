"""формирование весов слов для отлицательного словаря хи-квадрат"""
import csv
from itertools import zip_longest
import numpy as np
import pandas as pd


def scale(chi_square):
    return -1 * (chi_square - np.min(chi_square)) / (np.max(chi_square) - np.min(chi_square))


df = pd.read_csv('D:\\GitHub\\sentiment-analyzer\\app\\dictionaries\\original\\dict_collocations_minus.csv', encoding='utf-8')
chi = np.array(df['chi_square'])
chi_scaled = scale(chi)

words = df['term'].tolist()

d = [words, chi_scaled]
export_data = zip_longest(*d, fillvalue='')

with open('D:\\GitHub\\sentiment-analyzer\\app\\dictionaries\\chi_collocations_minus.csv', 'w', encoding='utf-8',
          newline='') as f:
    wr = csv.writer(f)
    wr.writerow(("term", "weight"))
    wr.writerows(export_data)
f.close()
