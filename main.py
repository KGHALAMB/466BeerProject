import pandas as pd
import matplotlib.pyplot as plt
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import LinearRegression

df = pd.read_csv('beer.csv', usecols=['Name', 'Style', 'ABV', 'Min IBU', 'Max IBU', 'Astringency', 'Hoppy', 'review_overall', 'number_of_reviews'])
#print(df.describe())

#print(df.head())

df = df.groupby('Style').plot.scatter(x="Astringency", y="review_overall")

print(df.head())


model = KNeighborsRegressor(5)
x_train = df[["Astringency"]]
y_train = df["review_overall"]

#model2 = LinearRegression()
#model2.fit(x_train, y_train)
#print(model2.coef_)
#print(model2.intercept_)
#print(model2.predict([[20]]))

model.fit(x_train, y_train)
print(model.predict([[70]]))
#df.plot.scatter(x="Astringency", y="review_overall")
#df.plot.scatter(x="review_overall", y="Min IBU")
#df.plot.scatter(x="review_overall", y="Hoppy")
#df.plot.scatter(x="review_overall", y="ABV")

plt.show()