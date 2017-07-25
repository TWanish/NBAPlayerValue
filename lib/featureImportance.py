# Determine least consequential data points

import numpy as np
import os, warnings

warnings.filterwarnings("ignore") #Suppress LDA warning

import pandas as pd

from sklearn.ensemble import RandomForestClassifier as RFC
from sklearn.model_selection import train_test_split as tts

path = os.path.normpath(str(os.getcwd()).split('lib')[0]+'data/nbaStats.csv')
data = pd.read_csv(path, engine='python')
data = data.drop(['mp'], axis=1)
data = data[data['g']>40]

classifier = RFC(n_estimators = 150, n_jobs = -1)

X = data.drop(['Player', 'Status', 'Pos', 'labels', 'X1', 'X2'], axis=1)
y = data['labels'].values


X_train, X_test, y_train, y_test = tts(X,y,test_size = 0.2)

classifier=classifier.fit(X_train, y_train)
predics = classifier.predict(X_test)

estims = pd.DataFrame(list(zip(list(X),
                               classifier.feature_importances_)),
                      columns=['Feature','Importance'])
estims = estims.sort_values('Importance', ascending=False)

print(estims)
                      
