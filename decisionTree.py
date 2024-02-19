import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn import tree
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import LinearRegression
from sklearn import metrics



df = pd.read_csv('beer.csv')

def help(x):
    if x > 4.5:
        return "Good"
    elif x > 3:
        return "Okay"
    else:
        return "Bad"

df["good_beer"] = df.apply(lambda x: help(x['review_overall']), axis=1)

print(df)

print(df.good_beer.value_counts())

attributes = ['ABV', 'Min IBU', 'Max IBU', 'Astringency', 'Body', 'Alcohol', 'Bitter', 'Sweet', 'Sour', 'Salty', 'Fruits', 'Hoppy', 'Spices', 'Malty']

df = df[df['number_of_reviews'] > 10]

X = df[attributes]
y = df['good_beer']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=5)

clf = DecisionTreeClassifier()
clf = clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)
print("Accuracy:",metrics.accuracy_score(y_test, y_pred))



#model2 = LinearRegression()
#model2.fit(x_train, y_train)
#print(model2.coef_)
#print(model2.intercept_)
#print(model2.predict([[20]]))

#model.fit(x_train, y_train)
#print(model.predict([[70]]))
#df.plot.scatter(x="Astringency", y="review_overall")
#df.plot.scatter(x="review_overall", y="Min IBU")
#df.plot.scatter(x="review_overall", y="Hoppy")
#df.plot.scatter(x="review_overall", y="ABV")

#plt.show()