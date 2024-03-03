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
X = data[['Country']]
#Encode any string data
encoder = OneHotEncoder()
X_encoded_sparse = encoder.fit_transform(X)

# Convert the sparse matrix to a dense matrix
X_encoded = X_encoded_sparse.toarray()

#Count number of countries in dataset
num_unique_countries = X['Country'].nunique()
print("Countries: %d"%num_unique_countries)

#Verify if the number of unique countries matches the number of columns after encoding
if num_unique_countries != X_encoded.shape[1]:
    print("Number of unique countries:", num_unique_countries)
    print("Number of columns after encoding:", X_encoded.shape[1])
    print("There seems to be a mismatch between the number of unique countries and the number of columns after encoding.")

# #Convert the encoded data back to a DataFrame
X_encoded_df = pd.DataFrame(X_encoded, columns=encoder.get_feature_names_out())

#Normalize the data
scaler = StandardScaler()
X = scaler.fit_transform(X_encoded_df)

#Perform K-means clustering
kmeans = KMeans(n_clusters=39)  # K = 39 for 39 unique countries in the dataset
kmeans.fit(X)
data['Cluster'] = kmeans.labels_
print(f"Cluster centers: {kmeans.cluster_centers_}")

#Analyze clusters
for cluster_label in range(kmeans.n_clusters):
    cluster_data = data[data['Cluster'] == cluster_label]
    print(f"Cluster {cluster_label}:")
    print(cluster_data.describe()[['ABV','Min IBU','Max IBU','Astringency','Bitter','Sweet','Sour','Fruits','Hoppy','Spices','Malty', 'review_overall']])

#Trying to use a real map
fig = plt.figure(figsize=(10,7))

#Creates the map
map = fig.add_subplot(1, 1, 1, projection=ccrs.LambertConformal())
map = plt.axes(projection=ccrs.PlateCarree())

#Add features to map
map.add_feature(cfeature.LAND)
map.add_feature(cfeature.OCEAN)
map.add_feature(cfeature.COASTLINE)
map.add_feature(cfeature.BORDERS, linestyle=':')

map.xaxis.set_visible(True)
map.yaxis.set_visible(True)

plt.scatter(data['Longitude'], data['Latitude'], c=data['Cluster'], cmap=plt.get_cmap("hsv"))
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('K-means Clustering By Country')
plt.show()