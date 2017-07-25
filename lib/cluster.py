import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.decomposition import PCA
from sklearn import cluster, metrics, datasets
from sklearn.preprocessing import StandardScaler
np.set_printoptions(precision=4)


def kmeans(reduced_data, n_clusters):
    #----Do KMeans clustering and return relevant graphing/performance data
    kmeans = cluster.KMeans(n_clusters=n_clusters, random_state=42)
    kmeans = kmeans.fit(reduced_data)
    sil_score = metrics.silhouette_score(reduced_data, kmeans.labels_, metric='euclidean')

    data_dictionary = {
        "labels": kmeans.labels_,
        "centroids": kmeans.cluster_centers_,
        "silhouette_score": sil_score
    }

    return data_dictionary

def agglom(reduced_data, n_clusters):
    #----Do Agglomerative clustering and return relevant performance data
    clustering = cluster.AgglomerativeClustering(n_clusters = n_clusters)
    clustering = clustering.fit(reduced_data)
    sil_score = metrics.silhouette_score(reduced_data, clustering.labels_, metric='euclidean')

    return {
        "labels":clustering.labels_,
        "silhouette_score": sil_score
        }

    
def find_best_cluster(cluster_type,data,a,b):
    #----Prints silhouette scores for all # of clusters in range
    scores = []
    for i in range(a,b):
        
        if cluster_type.lower() == "kmeans":
            i_clusters = kmeans(data, i)
        elif cluster_type.lower() == "agglom":
            i_clusters = agglom(data, i)
            
        sil_score_i = i_clusters['silhouette_score']
        scores.append(sil_score_i)

    print(scores)



def feature_importance(cluster_data, league_data, num_feats):
    #----Performs PCA and returns the stats with the least variance
    #----within each cluster, i.e. the common stats to a cluster
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(cluster_data)

    pca = PCA(n_components=2)
    PCA_reduced_df = pca.fit_transform(scaled_data)

    features = pd.DataFrame(list(zip(cluster_data.columns, pca.components_[0], np.mean(cluster_data), np.mean(league_data))),
        columns=['Feature', 'Importance', 'Cluster Average', 'League Average']).sort_values('Importance', ascending=True).head(10)

    return features


def plot_cluster(reduced_data, cluster_type, k_clusters, plot_title):
    if cluster_type.lower() == "kmeans":
        clus = KMeans(init='k-means++', n_clusters=k_clusters, n_init=10)

    elif cluster_type.lower() == "agglom":
        clus = AgglomerativeClustering(n_clusters = k_clusters)

    clus.fit(reduced_data)
    
    # Step size of the mesh. Decrease to increase the quality of the VQ.
    h = .02     # point in the mesh [x_min, x_max]x[y_min, y_max].

    # Plot the decision boundary. For that, we will assign a color to each
    x_min, x_max = reduced_data[:, 0].min() - 1, reduced_data[:, 0].max() + 1
    y_min, y_max = reduced_data[:, 1].min() - 1, reduced_data[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))

    # Obtain labels for each point in mesh. Use last trained model.
    Z = clus.predict(np.c_[xx.ravel(), yy.ravel()])

    # Put the result into a color plot
    Z = Z.reshape(xx.shape)
    plt.figure(1, figsize=(15,10))
    plt.clf()
    plt.imshow(Z, interpolation='nearest',
           extent=(xx.min(), xx.max(), yy.min(), yy.max()),
           cmap=plt.cm.Paired,
           aspect='auto', origin='lower')
    
    plt.plot(reduced_data[:, 0], reduced_data[:, 1], 'k.', markersize=10)

    if cluster_type.lower() == "kmeans":
        # Plot the centroids as a white X
        centroids = clus.cluster_centers_
        plt.scatter(centroids[:, 0], centroids[:, 1],
                marker='x', s=169, linewidths=3,
                color='w', zorder=10)
        
    plt.title(plot_title)
    plt.xlim(x_min, x_max)
    plt.ylim(y_min, y_max)
    plt.xticks(())
    plt.yticks(())
    plt.show()
