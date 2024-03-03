import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import StandardScaler


#Load the data
data = pd.read_csv('beer_with_locations.csv')

#Preprocess the data
data = data[data.Country == 'USA']
X = data[['Latitude', 'Longitude']]

#Perform K-means clustering
kmeans = KMeans(n_clusters=6)  #K = 6 for 6 US regions
kmeans.fit(X)
data['Cluster'] = kmeans.labels_
print(f"Cluster centers: {kmeans.cluster_centers_}")

#Analyze clusters
for cluster_label in range(kmeans.n_clusters):
    cluster_data = data[data['Cluster'] == cluster_label]
    print(f"Cluster {cluster_label}:")
    print(cluster_data.describe()[['ABV','Min IBU','Max IBU','Astringency','Bitter','Sweet','Sour','Fruits','Hoppy','Spices','Malty', 'review_overall']])

#Plot points on a real map
fig = plt.figure(figsize=(10,7))

#Creates the map
map = fig.add_subplot(1, 1, 1, projection=ccrs.LambertConformal())
map = plt.axes(projection=ccrs.PlateCarree())
map.set_extent([-2500000, 2500000, -2500000, 2500000], crs=ccrs.LambertConformal())
map.stock_img()

#Add features to map
map.add_feature(cfeature.LAND)
map.add_feature(cfeature.OCEAN)
map.add_feature(cfeature.COASTLINE)
map.add_feature(cfeature.BORDERS, linestyle=':')
map.add_feature(cfeature.STATES.with_scale('10m'))

map.xaxis.set_visible(True)
map.yaxis.set_visible(True)

plt.scatter(data['Longitude'], data['Latitude'], c=data['Cluster'], cmap=plt.get_cmap("viridis"))
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('K-means Clustering By Region')
plt.show()