import numpy as np
import pandas as pd
import warnings
import os

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from cluster import kmeans, find_best_cluster, feature_importance, plot_cluster, agglom

warnings.filterwarnings("ignore") #Suppress LDA warning
path = os.path.normpath(str(os.getcwd()).split('lib')[0]+'data/ncaaStats.csv')
data = pd.read_csv(path, engine='python')
data = data.drop(['MP'], axis=1)
data = data[data['G']>15]

#----Strategically specific data sets that add more variance than significance
X = data.drop(['Player', 'Pos', 'G', 'Status', 'School',
               'FG', 'FT', '2P', '2PA',
               '3P', '3PA', 'TRB','OWS',
               'BPM', 'DWS', 'WS/40', 'WS'], axis=1)
y = data['Pos']

#----Scale the data to reduce variance
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

#----Reducing remaining variables into 2
LDA = LinearDiscriminantAnalysis(n_components=2, shrinkage='auto', solver='eigen')
LDA_reduced_df = LDA.fit(X_scaled,y).transform(X_scaled)

print(LDA.score(X_scaled,y)) #Percentage of data captured by 2 variables

#----Determine best clustering method

kmeans = kmeans(LDA_reduced_df, 7)
#agglom = agglom(LDA_reduced_df, 7)

#find_best_cluster("kmeans",LDA_reduced_df,3,15)
#find_best_cluster("agglom",LDA_reduced_df,3,15)

#----Continuing forward with KMeans, notice drop off after 8 clusters.
#----So we'll use 8 as this number of clusters

data['Cluster'] = kmeans['labels']
y = kmeans['labels']
df = pd.DataFrame({'X1':LDA_reduced_df[:,0],'X2':LDA_reduced_df[:,1], 'labels':y})

#----Visualizes the clusters. Uncomment this if you want to see it.
#----This and its function is 100% taken from his project so I don't
#----like to use it. Program is too cluttered for me to worry about graphics. 
#plot_cluster(LDA_reduced_df, "kmeans", k_clusters=8, plot_title="""KMeans Clustering on NBA Players in 2012-2017""")

player_list = list(data['Player'])
status_list = list(data['Status'])

#----Display feature importance for each label
for i in range(0,7):
    mask = (data['Cluster'] == i)
    print("Cluster %d" % i)
    
    mask = (data['Cluster'] == i)
    print(data[mask][['Player']].head(10))

    #---- It reclusters the data to do this so we have to drop useless stats
    cluster_data = data[mask].drop(['Player', 'Pos', 
                                    'G', 'Status', 'School',
                                    'FG', 'FT', '2P', '2PA', '3P', '3PA',
                                    'TRB', 'OWS',
                                    'BPM','DWS', 'WS', 'WS/40', 'Cluster',
                                    'Status'], axis=1)
    league_data = data.drop(['Player', 'Pos', 'G',
                             'Status', 'FG', 'FT', 'School',
                             '2P', '2PA', '3P', '3PA',
                             'TRB', 'OWS', 'BPM', 'DWS', 'WS', 
                             'WS/40', 'Cluster', 'Status'], axis=1)
    print(feature_importance(cluster_data, league_data, 10).reset_index().drop('index', axis=1))

#----Replace the label numbers with the player roles
df['Player'] = player_list
df['Status'] = status_list
df['labels'] = df['labels'].map({0: 'Swingman',
                                 1: 'Scoring Wing',
                                 2: 'Game Manager',
                                 3: 'Defensive Big',
                                 4: 'Versatile Forward',
                                 5: 'Offensive Big',
                                 6: 'Shooting Wing'})


#---- Write the results to a csv
path = os.path.normpath(str(os.getcwd()).split('lib')[0]+'data/ncaa_positions.csv')

df.to_csv(path)
