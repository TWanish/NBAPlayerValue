import numpy as np
import os
import warnings
import matplotlib.pyplot as plt
import matplotlib

warnings.filterwarnings("ignore") #Suppress LDA warning

import pandas as pd

from sklearn.model_selection import train_test_split as tts
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
from sklearn.naive_bayes import GaussianNB

path = os.path.normpath(str(os.getcwd()).split('lib')[0]+'data/nbaStats.csv')
nbaData = pd.read_csv(path, engine='python')
nbaData = nbaData[nbaData['g']>40]

path = os.path.normpath(str(os.getcwd()).split('lib')[0]+'data/ncaaStats.csv')
ncaaData = pd.read_csv(path, engine='python')
ncaaData = ncaaData[ncaaData['G']>15]

#----Position Based Analysis and Graphic Creation
positions = ['C','PF','SF','PG','SF']
ncaaPos = ['Center', 'Forward', 'Guard']

nbaCount = []
for x in positions:
    nbaCount.append(len(nbaData[nbaData['Pos']==x]))
ncaaCount = []
for x in ncaaPos:
    ncaaCount.append(len(ncaaData[ncaaData['Pos']==x]))

sumNba = sum(nbaCount)
sumNcaa = sum(ncaaCount)

nbaRatios = [round(x/float(sumNba),2) for x in nbaCount]
ncaaRatios = [x/float(sumNcaa) for x in ncaaCount]
ncaaRatios.extend([None,None])

expNcaaRatios = [
    nbaRatios[0]+.3*nbaRatios[1],
    .70*nbaRatios[1]+.85*nbaRatios[2],
    .15*nbaRatios[2] + nbaRatios[3] + nbaRatios[4], None, None
    ]
data = {
    'Pos':positions,
    'nbaRatios':nbaRatios,
    'expNcaaRatios':expNcaaRatios,
    'realNcaaRatios': ncaaRatios
        }

df = pd.DataFrame.from_dict(data)
df = df[['Pos','nbaRatios', 'expNcaaRatios', 'realNcaaRatios']]

index = range(0,5)
plt.barh(index,nbaRatios,align='center',alpha=0.5)
plt.yticks(index,positions)
plt.xlabel('% of total players')
plt.title('NBA Position Ratios')
axes = plt.gca()
axes.set_xlim([0,0.6])
plt.show()

fig, ax = plt.subplots()
index = range(0,3)
bar_width = .35
opacity = 0.5

rects1 = plt.barh(index, expNcaaRatios[0:3], bar_width, alpha=opacity,
                  label = 'Expected')
index = [x+bar_width for x in index]
rects2 = plt.barh(index, ncaaRatios[0:3], bar_width, alpha=opacity,
                  label = 'Real')
index = [x-(bar_width/2) for x in index]
plt.yticks(index, ['C', 'F', 'G'])
plt.legend()
plt.xlabel('% of total players')
plt.title('NCAA Position Ratios')
axes = plt.gca()
axes.set_xlim([0,0.6])
plt.show()

matplotlib.rcParams.update({'font.size': 8})

#----Label Based analysis and Graphic Creation

nbaLabels = [
    'Scoring Center', 'Supporting Center', 'Versatile Forward',
    '3-and-D Wing', 'Scoring Wing', 'Shooting Wing', 'Combo Guard',
    'Floor General'
    ]

ncaaLabels = [
    'Offensive Big', 'Defensive Big', 'Versatile Forward', 'Scoring Wing',
    'Shooting Wing', 'Swingman', 'Game Manager'
    ]

nbaLCount = []
for x in nbaLabels:
    nbaLCount.append(len(nbaData[nbaData['labels']==x]))

nbaLRatios = [round(x/float(sumNba),2) for x in nbaLCount]
tempSum = sum(nbaLRatios)
nbaLRatios = [x/float(tempSum) for x in nbaLRatios]

index = range(0,len(nbaLabels))
plt.barh(index,nbaLRatios,align='center',alpha=0.5)
plt.yticks(index,nbaLabels)
plt.xlabel('% of total players')
plt.title('NBA Player Role Ratios')
axes = plt.gca()
axes.set_xlim([0,.30])
plt.show()

ncaaLCount = []
for x in ncaaLabels:
    ncaaLCount.append(len(ncaaData[ncaaData['labels']==x]))
    
ncaaLRatios = [x/float(sumNcaa) for x in ncaaLCount]

#--Correct ncaa based on distribution vs expected
ncaaCRatio = expNcaaRatios[0]/ncaaRatios[0]
ncaaFRatio = expNcaaRatios[1]/ncaaRatios[1]
ncaaGRatio = expNcaaRatios[2]/ncaaRatios[2]

adjNcaaLRatios = [
    ncaaLRatios[0]*(ncaaCRatio*.60+.40*ncaaFRatio),
    ncaaLRatios[1]*(ncaaCRatio*.80+.2*ncaaFRatio),
    ncaaLRatios[2]*ncaaFRatio, ncaaLRatios[3]*(.8*ncaaFRatio + .2*ncaaGRatio),
    ncaaLRatios[4]*(.5*ncaaFRatio + .5*ncaaGRatio),
    ncaaLRatios[5]*(.3*ncaaFRatio + .7*ncaaGRatio), ncaaLRatios[6]*ncaaGRatio
    ]
tempSum = sum(adjNcaaLRatios)
adjNcaaLRatios = [x/tempSum for x in adjNcaaLRatios]

fig, ax = plt.subplots()
index = range(0,len(ncaaLRatios))
bar_width = .35
opacity = 0.5

rects1 = plt.barh(index, adjNcaaLRatios, bar_width, alpha=opacity,
                  label = 'Adjusted')
index = [x+bar_width for x in index]
rects2 = plt.barh(index, ncaaLRatios, bar_width, alpha=opacity,
                  label = 'Raw')
index = [x-(bar_width/2) for x in index]
plt.yticks(index, ncaaLabels)
plt.legend()
plt.xlabel('% of total players')
plt.title('NCAA Player Role Ratios')
axes = plt.gca()
axes.set_xlim([0,0.3])
plt.show()
    
#--Revis using pie chart for readability

plt.pie(nbaLRatios,labels=nbaLabels,startangle=90)
plt.axis('equal')
plt.title('NBA Player Role Ratios')
plt.show()

plt.pie(adjNcaaLRatios, labels=ncaaLabels,startangle=90)
plt.axis('equal')
plt.title('NCAA Player Role Ratios')
plt.show()

#----Find players both in NCAA and NBA
nbaPlayLabels = nbaData[['Player','labels', 'X1', 'X2']]
bothPlayers = pd.DataFrame.merge(ncaaData,nbaPlayLabels, on=['Player'], how='inner')
classifier = GaussianNB()
print(bothPlayers.head())
X = bothPlayers.drop(['Player', 'labels_y','X1_y','X2_y',
                      'Status', 'G', 'MP', 'School',
                      'PER','OWS','DWS','WS','WS/40','BPM'], axis=1)
X['Pos'] = X['Pos'].map({'Center':5,
                         'Center-Forward':4,
                         'Forward-Center':4,
                         'Forward':3,
                         'Forward-Guard':2,
                         'Guard-Forward':2,
                         'Guard':1})   
X['labels_x'] = X['labels_x'].map({'Swingman':0,
                                   'Scoring Wing':1,
                                   'Game Manager':2,
                                   'Defensive Big':3,
                                   'Versatile Forward':4,
                                   'Offensive Big':5,
                                   'Shooting Wing':6})
y = bothPlayers['labels_y'].values
scaler = StandardScaler()
X_fix = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = tts(X,y,test_size = 0.2)

classifier=classifier.fit(X_train, y_train)
predics = classifier.predict(X_test)
#print('NBA role prediction accuracy is %f' % accuracy_score(predics, y_test))

draftClass = ['Markelle Fultz', 'Lonzo Ball', 'Jayson Tatum',
              'Josh Jackson', "De'Aaron Fox", 'Jonathan Isaac',
              'Lauri Markkanen', 'Dennis Smith Jr.', 'Zach Collins',
              'Malik Monk', 'Luke Kennard', 'Donovan Mitchell',
              'Bam Adebayo', 'Justin Jackson', 'Justin Patton',
              'D.J. Wilson', 'T.J. Leaf', 'John Collins',
              'Harry Giles', 'Jarrett Allen', 'OG Anunoby',
              'Tyler Lydon', 'Caleb Swanigan', 'Kyle Kuzma',
              'Tony Bradley', 'Derrick White', 'Josh Hart',
              'Frank Jackson', 'Davon Reed', 'Wesley Iwundu',
              'Frank Mason III', 'Ivan Rabb', 'semi Ojeleye',
              'Jordan Bell', 'Jawun Evans', 'Dwayne Bacon',
              'Tyler Dorsey', 'Thomas Bryant', 'Damyean Dotson',
              'Dillon Brooks', 'Sterling Brown', 'Ike Anigbogu',
              'Sindarius Thornwell', 'Monte Morris', 'Edmond Sumner',
              'Kadeem Allen', 'Alec Peters', 'Nigel Williams-Goss',
              'Jabari Bird', 'Jaron Blossomgame']

predDraftClass = ncaaData[ncaaData['Player'].isin(draftClass)]
predDraftClass = predDraftClass.drop(['Status', 'G',
                                      'MP', 'School', 
                                      'PER','OWS','DWS','WS',
                                      'WS/40','BPM'], axis=1)
predDraftClass['Pos'] = predDraftClass['Pos'].map({'Center':5,
                                                 'Center-Forward':4,
                                                 'Forward-Center':4,
                                                 'Forward':3,
                                                 'Forward-Guard':2,
                                                 'Guard-Forward':2,
                                                 'Guard':1})   
predDraftClass['labels'] = predDraftClass['labels'].map({'Swingman':0,
                                                           'Scoring Wing':1,
                                                           'Game Manager':2,
                                                           'Defensive Big':3,
                                                           'Versatile Forward':4,
                                                           'Offensive Big':5,
                                                           'Shooting Wing':6})
predDraftClass['predicted_role']=classifier.predict(predDraftClass.drop(['Player'],
                                                                         axis = 1))
predDraftClass['Pos'] = predDraftClass['Pos'].map({5:'Center',
                                                 4:'Center-Forward',
                                                 3:'Forward',
                                                 2:'Forward-Guard',
                                                 1:'Guard'})   
predDraftClass['labels'] = predDraftClass['labels'].map({0:'Swingman',
                                                           1:'Scoring Wing',
                                                           2:'Game Manager',
                                                           3:'Defensive Big',
                                                           4:'Versatile Forward',
                                                           5:'Offensive Big',
                                                           6:'Shooting Wing'})

predDraftClass = predDraftClass[['Player','Pos','labels','predicted_role']]
#predDraftClass.to_csv('predictions.csv')
