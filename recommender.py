import pandas as pd
from sklearn.metrics import f1_score
from sklearn.neighbors import NearestNeighbors
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import warnings
warnings.filterwarnings("ignore", message="X does not have valid feature names, but StandardScaler was fitted with feature names", category=UserWarning)


df = pd.read_csv('beer.csv')
filtered_data = df[df['number_of_reviews'] > 10]

#filter and clean data. 80% train 20% test
attributes = ['ABV', 'Min IBU', 'Max IBU', 'Astringency', 'Body', 'Alcohol', 'Bitter', 'Sweet', 'Sour', 'Salty', 'Fruits', 'Hoppy', 'Spices', 'Malty']
X = filtered_data[attributes]

#standardize, model, and fit
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
knn_model = NearestNeighbors(n_neighbors=5, algorithm='ball_tree')
knn_model.fit(X_scaled)


def recommend_similar_beers(liked_beers, user,  n_neighbors=1):
    liked_beers_scaled = scaler.transform(liked_beers)  #scale

    distances, indices = knn_model.kneighbors(liked_beers_scaled, n_neighbors=n_neighbors) #neighbors

    recommended_indices = indices.flatten()
    recommended_beers = filtered_data.iloc[recommended_indices]

    #remove beers they have already tried
    recommended_beers = recommended_beers[~recommended_beers['Name'].isin(user['Beer Name'])]

    # Goal to return 5 recommendations, if all nearest neighbors have
    # been tried by user, increase neighbors
    if(len(recommended_beers) < (5)):
        n_neighbors += 1
        return recommend_similar_beers(liked_beers, user, n_neighbors)
    return recommended_beers


# add user's ratings to the model's dataframe
user = pd.read_csv('beerUser1.csv')
user = user[['Beer Name', 'Their Rating']]
# print(user)

user['Their Rating'] = user.groupby('Beer Name')['Their Rating'].transform('mean')
user.drop_duplicates(inplace = True)
user['Their Rating'] = sorted(user['Their Rating'], reverse=True)
user = user[['Beer Name', 'Their Rating']]
# user = user[user['Their Rating'] > 4]
# print(user)
attributes2 = ['ABV', 'Min IBU', 'Max IBU', 'Astringency', 'Body', 'Alcohol', 'Bitter', 'Sweet', 'Sour', 'Salty', 'Fruits', 'Hoppy', 'Spices', 'Malty', 'Their Rating']

merged_df = filtered_data.merge(user, left_on='Name', right_on='Beer Name', how='left')
merged_df.drop_duplicates(inplace = True)
merged_df['Their Rating'] = sorted(merged_df['Their Rating'], reverse=True)

merged_df = merged_df.head(2) #get users top 2 reviews
print("Your top 2 beers are: \n", merged_df[['Name', 'number_of_reviews', 'review_overall', 'Their Rating']])

liked_beers = merged_df[attributes].values



recommended_beers = recommend_similar_beers(liked_beers, user)
import pandas as pd

def map_reviews(input):
    r = 1
    if input > 1000:
        r = 10
    elif input > 500:
        r = 7
    elif input > 100:
        r = 5
    elif input > 50:
        r = 3
    elif input > 20:
        r = 2
    return r

new_reviews = recommended_beers['number_of_reviews'].apply(map_reviews)

new_reviews = pd.DataFrame({'Score': new_reviews})
recommended_beers['Score'] = new_reviews['Score']

#I did the F1 calculation
new_ratings = (recommended_beers['Score'] * recommended_beers['review_overall']) / (recommended_beers['Score'] + recommended_beers['review_overall'])

# Assign the new ratings to the 'new' column
recommended_beers['Score'] = new_ratings

# Sort the DataFrame by the 'new' column
recommended_beers = recommended_beers.sort_values(by='Score', ascending=False)

print("Your recommended new beers: ")
print(recommended_beers[['Name', 'number_of_reviews', 'review_overall', 'Score']])

