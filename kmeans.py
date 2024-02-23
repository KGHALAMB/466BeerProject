import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# Step 1: Load the data
data = pd.read_csv('beer_with_locations.csv')

# Step 2: Preprocess the data
X = data[['Latitude', 'Longitude']]

# Step 3: Perform K-means clustering
kmeans = KMeans(n_clusters=6)  # Specify the number of clusters
kmeans.fit(X)
data['Cluster'] = kmeans.labels_

# Step 4: Analyze clusters
for cluster_label in range(kmeans.n_clusters):
    cluster_data = data[data['Cluster'] == cluster_label]
    print(f"Cluster {cluster_label}:")
    print(cluster_data.describe())

# Visualize clusters
plt.scatter(data['Longitude'], data['Latitude'], c=data['Cluster'], cmap='viridis')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('K-means Clustering')
plt.show()
