import pandas as pd

df = pd.read_csv('beer.csv')

# df = df["beer_name", "review_overall", "review_aroma", "review_appearance", "review_palate", "review_taste", "beer_style", "beer_abv",]

print(df.head())

