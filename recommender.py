import pandas as pd
from sklearn.metrics import f1_score
from sklearn.neighbors import NearestNeighbors
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split


df = pd.read_csv('beer.csv')
filtered_data = df[df['number_of_reviews'] > 10]

#filter and clean data. 80% train 20% test
attributes = ['ABV', 'Min IBU', 'Max IBU', 'Astringency', 'Body', 'Alcohol', 'Bitter', 'Sweet', 'Sour', 'Salty', 'Fruits', 'Hoppy', 'Spices', 'Malty']
X = filtered_data[attributes]
#standardize, model, fit
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
knn_model = NearestNeighbors(n_neighbors=5, algorithm='ball_tree')
knn_model.fit(X_scaled)


def recommend_similar_beers(liked_beers, user,  n_neighbors=1):
    liked_beers_scaled = scaler.transform(liked_beers)  #scale
    distances, indices = knn_model.kneighbors(liked_beers_scaled, n_neighbors=n_neighbors)  # Find nearest neighbors

    recommended_indices = indices.flatten()
    recommended_beers = filtered_data.iloc[recommended_indices]
    # already_rated = recommended_beers['Name'].isin(user['Beer Name'])
    recommended_beers = recommended_beers[~recommended_beers['Name'].isin(user['Beer Name'])]

    if(len(recommended_beers) < (5)):
        n_neighbors +=1
        return recommend_similar_beers(liked_beers, user, n_neighbors)
    return recommended_beers


user = pd.read_csv('beerUser1.csv')
user = user[['Beer Name', 'Their Rating']]
# print(user)

user['Their Rating'] = user.groupby('Beer Name')['Their Rating'].transform('mean')
user.drop_duplicates(inplace = True)
user['Their Rating'] = sorted(user['Their Rating'], reverse=True)
user = user[['Beer Name', 'Their Rating']]
user = user[user['Their Rating'] > 4]
# print(user)

merged_df = filtered_data.merge(user, left_on='Name', right_on='Beer Name', how='left')
merged_df.dropna(inplace = True)
merged_df.drop_duplicates(inplace = True)
merged_df['Their Rating'] = sorted(merged_df['Their Rating'], reverse=True)

merged_df = merged_df.head(2)

# Example of usage:
liked_beers = merged_df[attributes].values

recommended_beers = recommend_similar_beers(liked_beers, user)
recommended_beers['number_of_reviews'] = sorted(recommended_beers['number_of_reviews'], reverse=True)

print("Your recommended new beers: ")
print(recommended_beers[['Name', 'number_of_reviews']])
