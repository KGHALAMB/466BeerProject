import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np

#Load the data
data = pd.read_csv('beer_with_locations.csv')

#Preprocess the data
data = data[data.Country == 'USA']

#Exploratory visual analysis
#Trying to use a real map
fig = plt.figure(figsize=(10,7))

#Creates the map
map = fig.add_subplot(1, 1, 1, projection=ccrs.LambertConformal())
map = plt.axes(projection=ccrs.PlateCarree())
map.set_extent([-2500000, 2500000, -2500000, 2500000], crs=ccrs.LambertConformal())
#Sets background image
map.stock_img()

#Adds features to map
map.add_feature(cfeature.LAND)
map.add_feature(cfeature.OCEAN)
map.add_feature(cfeature.COASTLINE)
map.add_feature(cfeature.BORDERS, linestyle=':')
map.add_feature(cfeature.LAKES, alpha=0.5)
map.add_feature(cfeature.RIVERS)
map.add_feature(cfeature.STATES.with_scale('10m'))

map.xaxis.set_visible(True)
map.yaxis.set_visible(True)

#Plots the data onto map
plt.scatter(data['Longitude'], data['Latitude'], alpha=0.4, 
            s=data['number_of_reviews']/10, label="number of reviews",
            c=data['review_overall'], 
            cmap=plt.get_cmap("jet"), 
            transform=ccrs.PlateCarree())

# Colorbar
reviews = data["review_overall"]
tick_values = np.linspace(0, 5, 7)
cbar = plt.colorbar()
cbar.ax.set_yticklabels(["%d stars"%v for v in tick_values], fontsize=14)
cbar.set_label('Overall Rating', fontsize=16)

# Plot labels
plt.title('Beer Ratings Across the US')
plt.ylabel("Latitude", fontsize=14)
plt.xlabel("Longitude", fontsize=14)
plt.show()