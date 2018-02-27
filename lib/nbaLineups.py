import numpy as np
import warnings
import os
import pandas as pd


lineupPath = os.path.normpath(str(os.getcwd()).split('lib')[0]+'data//lineups_16_17.csv')
statsPath = os.path.normpath(str(os.getcwd()).split('lib')[0]+'data//nbaStats.csv')
luData = pd.read_csv(lineupPath, engine='python')
stData = pd.read_csv(statsPath, engine='python')

fp = list(luData['First Player'])
sp = list(luData['Second Player'])
tp = list(luData['Third Player'])
fop = list(luData['Fourth Player'])
fip = list(luData['Fifth Player'])
labels = list(stData['labels'])
status = list(stData['Status'])
actualStats = luData.drop(['First Player', 'Second Player',
                           'Third Player', 'Fourth Player', 'Fifth Player',
                           'TEAM', 'Unnamed: 0'],axis=1)
playerNum = ['First Player', 'Second Player', 'Third Player', 'Fourth Player',
                 'Fifth Player']

lineups = []
labelLineups = []

#----Collect List of Lineups 
for i in range(0, len(fp)):
    lineups.append([fp[i], sp[i], tp[i], fop[i], fip[i]])

                  
luNames = []
plNames = stData['Player']

#----Convert Player Fullnames to the Lineup Data Format
for name in list(plNames):
    luNames.append(name[0:1]+'.' + name.split(' ')[1])

#----Compare lineup names to converted names and pull relevant labels
for name in lineups:
    labelEntry = []
    for i in range(0,5):
        for j in range(0,len(luNames)):
            if name[i].strip() == luNames[j] and status[j]=='Active':
                labelEntry.append(labels[j])
                break
    labelLineups.append(labelEntry)


lineupMasked = pd.DataFrame(labelLineups, columns = ['First Player',
                                                        'Second Player',
                                                        'Third Player',
                                                        'Fourth Player',
                                                        'Fifth Player'])
lineupMasked = pd.concat([lineupMasked, actualStats], axis=1)

for pNum in playerNum:
    lineupMasked[pNum]=lineupMasked[pNum].map({'Supporting Center':1,
                                               'Scoring Center':10,
                                               'Versatile Forward':100,
                                               '3-and-D Wing':1000,
                                               'Shooting Wing':10000,
                                               'Scoring Wing':100000,
                                               'Combo Guard':1000000,
                                               'Floor General':10000000})
lineupMasked['Lineup Number'] = (lineupMasked['First Player'] +
                                 lineupMasked['Second Player'] +
                                 lineupMasked['Third Player'] +
                                 lineupMasked['Fourth Player'] +
                                 lineupMasked['Fifth Player'])
lineupMasked['Total Min'] = lineupMasked['GP']*lineupMasked['MIN']
lineupMasked=lineupMasked.drop(['First Player', 'Second Player',
                                'Third Player', 'Fourth Player',
                                'Fifth Player', 'GP', 'MIN'],axis=1)

#----Match lineup numbers, filter out minimum min played, sort by +/-
avgData = lineupMasked.groupby('Lineup Number').mean()
avgData['Total Min'] = lineupMasked.groupby('Lineup Number').sum()['Total Min'].values
avgData = avgData[avgData['Total Min']>100]
avgData = avgData.sort_values('+/-',ascending = False)

#----Breaking back out into individual player roles from lineup number
lineupNums = avgData.index.values.tolist()
mappings = {10000000:'Floor General',
            1000000: 'Combo Guard',
            100000: 'Scoring Wing',
            10000: 'Shooting Wing',
            1000: '3-and-D Wing',
            100: 'Versatile Forward',
            10: 'Scoring Center',
            1: 'Supporting Center'}
lineupsUnmasked = []
appendRow = [0, 0, 0, 0, 0]
for i in range(0,len(lineupNums)):
    for j in range(0,5):
        for key in sorted(mappings.keys(), reverse = True):
            if int(lineupNums[i] / key) >= 1:
                appendRow[j] = (mappings[key])
                lineupNums[i] -= key
                break
    lineupsUnmasked.append(appendRow[:])

lineupRankings = pd.DataFrame(lineupsUnmasked, columns = ['First Player',
                                                          'Second Player',
                                                          'Third Player',
                                                          'Fourth Player',
                                                          'Fifth Player'])
for pNum in playerNum:
    avgData[pNum] = lineupRankings[pNum].values


#----Write to CSV
#endPath = os.path.normpath(str(os.getcwd()).split('lib')[0]+'data/bestLineups.csv')
#avgData.to_csv(endPath, index= False)

##### Will require manual cleanup due to format of lineup data (Seth Curry
##### and Steph Curry are both S.Curry. Can fix if you include a list of
##### teams the player has played on in NBA Stats and compare that with
##### the team listed in lineups. Will do to improve overall composition of
##### project. Advanced stats implementation also necessary

#--------TODO
# Implement Advanced/Rate stats, Manual clean up
# Compare
# Optimize program cause there's no way this is

        


