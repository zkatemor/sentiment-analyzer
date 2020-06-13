import pandas as pd
from pandas_ml import ConfusionMatrix

data = {'y_Actual':    ['Yes', 'No',  'No', 'Yes', 'No', 'Yes', 'No',  'No', 'Yes', 'No', 'Yes', 'No'],
        'y_Predicted': ['Yes', 'Yes', 'No', 'Yes', 'No', 'Yes', 'Yes', 'No', 'Yes', 'No', 'No',  'No']
        }

df = pd.DataFrame(data, columns=['y_Actual','y_Predicted'])
df['y_Actual'] = df['y_Actual'].map({'Yes': 1, 'No': 0})
df['y_Predicted'] = df['y_Predicted'].map({'Yes': 1, 'No': 0})

Confusion_Matrix = ConfusionMatrix(df['y_Actual'], df['y_Predicted'])
Confusion_Matrix.print_stats()