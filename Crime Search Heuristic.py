import matplotlib.pyplot as plt
import seaborn as sns
sns.set()
from sklearn.cluster import KMeans
from scipy.spatial.distance import cdist
import pandas as pd
from kneed import KneeLocator

# checks distance from crime cluster center to given geocode
#clusters based on longitude and latitude


# #plot of crime count by lat, long 
# plt.scatter(crime['Longitude'],crime['Latitude'])

# plt.xlim(-74.04,-73.9)
# plt.ylim(40.65,40.9)
# plt.show()

def cluster(crime):
    x = crime.iloc[:,8:10] # 1t for rows and second for columns

    # # fitting kmeans to predict for dataset
    # kmeans = KMeans(5)
    # kmeans.fit(x)

    # clusters = kmeans.fit_predict(x)

    # clusters
    wcss=[]
    for i in range(1,10):
        kmeans = KMeans(i)
        kmeans.fit(x)
        wcss_iter = kmeans.inertia_
        wcss.append(wcss_iter)

    # #determine # of clusters using elbow method

    k1 = KneeLocator(range(1, 10), wcss, curve="convex", direction="decreasing")
    # print("number of clusters: ", k1.elbow)

    #plot of clusters using k = 3 as # of clusters
    kmeans = KMeans(3)
    kmeans.fit(x)
    clusters = kmeans.fit_predict(x)

    data_with_clusters = crime.copy()
    data_with_clusters['Clusters'] = clusters 
    # plt.scatter(data_with_clusters['Longitude'],data_with_clusters['Latitude'],c=data_with_clusters['Clusters'],cmap='autumn')

    #count per cluster

    # cluster_labels = kmeans.fit_predict(x)
    # cluster_counts = Counter(cluster_labels)

    # print("count per cluster", cluster_counts)
    # #find center of each cluster

    centers = kmeans.cluster_centers_
    # print ("centers: ", centers)
    #plt.scatter(centers[:, 0], centers[:, 1], c='black', alpha=0.5);

    # center_1 = centers[0]
    # center_2 = centers[1]
    # center_3 = centers[2]

    radii = [cdist(x[clusters==i],[center],metric='euclidean').max() for i,center in enumerate(centers)]
    # print(radii)

    return centers, radii
# def distance(crime_loc_1: tuple, crime_loc_2: tuple, crime_loc_3:tuple, destination:tuple):
#     '''
#     takes geocode of crime cluster centers and destination to 
#     determine the distance between the two points for each center
#     '''
    
#     distance_1 = API_functions.get_distance([crime_loc_1], [destination])
#     distance_2 = API_functions.get_distance([crime_loc_2], [destination])
#     distance_3 = API_functions.get_distance([crime_loc_3], [destination])

#     return distance_1, distance_2, distance_3

