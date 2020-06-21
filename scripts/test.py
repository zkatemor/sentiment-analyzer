import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report
import seaborn as sn

from app.services.sentimental import Sentimental


def get_report_test(dictionary, is_unigram):
    # результат классификации
    prediction = []
    # реальный результат
    actual = []

    sent = Sentimental(dictionary=dictionary,
                       negation='D:\\GitHub\\sentiment-analyzer\\app\\dictionaries\\negations.csv',
                       modifier='D:\\GitHub\\sentiment-analyzer\\app\\dictionaries\\modifier.csv',
                       is_unigram=is_unigram)

    for i in range(0, len(texts)):
        result = sent.analyze(texts[i])

        if ratings[i] in range(4, 6):
            actual.append('positive')
            if result['score'] > 0:
                prediction.append('positive')
            elif result['score'] <= 0:
                prediction.append('negative')
        else:
            actual.append('negative')
            if result['score'] > 0:
                prediction.append('positive')
            elif result['score'] <= 0:
                prediction.append('negative')

        print(i)

    print(classification_report(actual, prediction))
    return prediction, actual


# загрузка тестового набора данных
df = pd.read_excel('D:\\GitHub\\sentiment-analyzer\\app\static\\reviews.xlsx', sheet_name="Sheet1")
texts = df['Text'].tolist()
ratings = df['Rating'].tolist()

dictionary_rusentilex = ['D:\\GitHub\\sentiment-analyzer\\app\\dictionaries\\rusentilex.csv']

dictionary_chi = ['D:\\GitHub\\sentiment-analyzer\\app\\dictionaries\\chi_minus.csv',
                  'D:\\GitHub\\sentiment-analyzer\\app\\dictionaries\\chi_plus.csv']

dictionary_cnn = ['D:\\GitHub\\sentiment-analyzer\\app\\dictionaries\\cnn_dict.csv']

dictionary_chi_collocations = ['D:\\GitHub\\sentiment-analyzer\\app\\dictionaries\\chi_collocations_minus.csv',
                               'D:\\GitHub\\sentiment-analyzer\\app\\dictionaries\\chi_collocations_plus.csv']

prediction, actual = get_report_test(dictionary_chi, True)

data = {'prediction': prediction,
        'actual': actual
        }

df = pd.DataFrame(data, columns=['actual', 'prediction'])
matrix = pd.crosstab(df['actual'], df['prediction'], rownames=['Actual'], colnames=['Predicted'])
print(matrix)
plt.figure(figsize=(10, 7))
sn.heatmap(matrix, annot=True, cmap="Greens")
plt.title("CHI UNIGRAM")
plt.show()
