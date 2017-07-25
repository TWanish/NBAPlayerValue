import numpy as np
import warnings
import os

warnings.filterwarnings("ignore") #Suppress LDA warning

import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from cluster import kmeans, find_best_cluster, feature_importance, plot_cluster, agglom

path = os.path.normpath(str(os.getcwd()).split('lib')[0]+'data/nbaStats.csv')
data = pd.read_csv(path, engine='python')
data = data.drop(['mp'], axis=1)
data = data[data['g']>40]

#----Strategically specific data sets that add more variance than significance
X = data.drop(['Player','labels', 'X1', 'X2', 'Pos', 'g', 'Status',
               'fg3a_heave', 'fg3_heave', 'FG', 'FT', '2P', '2PA',
               '3P', '3PA', 'fg2_dunk', 'ORB', 'DRB', 'TRB','OWS',
               'BPM', 'DWS', 'WS/48', 'WS','VORP'], axis=1)
y = data['Pos']

#----Scale the data to reduce variance
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

#----Reducing remaining variables into 2
LDA = LinearDiscriminantAnalysis(n_components=2, shrinkage='auto', solver='eigen')
LDA_reduced_df = LDA.fit(X_scaled,y).transform(X_scaled)

print(LDA.score(X_scaled,y)) #Percentage of data captured by 2 variables

#----Determine best clustering method

kmeans = kmeans(LDA_reduced_df, 8)
agglom = agglom(LDA_reduced_df, 8)

find_best_cluster("kmeans",LDA_reduced_df,5,20)
find_best_cluster("agglom",LDA_reduced_df,5,20)

#----Continuing forward with KMeans, notice drop off after 8 clusters.
#----So we'll use 8 as this number of clusters

data['Cluster'] = kmeans['labels']
y = kmeans['labels']
df = pd.DataFrame({'X1':LDA_reduced_df[:,0],'X2':LDA_reduced_df[:,1], 'labels':y})
#--X1 increases with TRB%, PF, %2FG Ast, %2FGA of FGA
#--X1 decreases with AST%, Avg Dist, FT%,
#--X2 increases with TOV%, 2Pt Att%, 0-3FGA%
#--X2 decreases with Ast FG%, Corner 3%, %3PA of FGA


#----Visualizes the clusters. Uncomment this if you want to see it.
#----This and its function is 100% taken from his project so I don't
#----like to use it. Program is too cluttered for me to worry about graphics. 
#plot_cluster(LDA_reduced_df, "kmeans", k_clusters=8, plot_title="""KMeans Clustering on NBA Players in 2012-2017""")

player_list = list(data['Player'])
status_list = list(data['Status'])

#----Display feature importance for each label
for i in range(0,8):
    mask = (data['Cluster'] == i)
    print("Cluster %d" % i)
    
    mask = (data['Cluster'] == i)
    print(data[mask][['Player']].head(10))

    #---- It reclusters the data to do this so we have to drop useless stats
    cluster_data = data[mask].drop(['Player', 'Pos', 'X1', 'X2', 'labels',
                                    'g', 'Status', 'fg3a_heave', 'fg3_heave',
                                    'FG', 'FT', '2P', '2PA', '3P', '3PA',
                                    'fg2_dunk', 'ORB', 'DRB', 'TRB', 'OWS',
                                    'BPM','DWS', 'WS', 'VORP','WS/48', 'Cluster',
                                    'Status'], axis=1)
    league_data = data.drop(['Player', 'Pos', 'X1', 'X2', 'labels',
                             'g', 'Status', 'fg3a_heave', 'fg3_heave', 'FG',
                             'FT', '2P', '2PA', '3P', '3PA', 'fg2_dunk', 'ORB',
                             'DRB', 'TRB', 'OWS', 'BPM', 'DWS', 'WS', 'VORP',
                             'WS/48', 'Cluster', 'Status'], axis=1)
    
    print(feature_importance(cluster_data, league_data, 10).reset_index().drop('index', axis=1))

#----Replace the label numbers with the player roles
df['Player'] = player_list
df['Status'] = status_list
df['labels'] = df['labels'].map({0: 'Versatile Forward',
                                 1: 'Scoring Wing',
                                 2: 'Supporting Center',
                                 3: '3-and-D Wing',
                                 4: 'Floor General',
                                 5: 'Shooting Wing',
                                 6: 'Combo Guard',
                                 7: 'Scoring Center'})


#---- Write the results to a csv
path = os.path.normpath(str(os.getcwd()).split('lib')[0]+'data/nba_positions.csv')

df.to_csv(path)
