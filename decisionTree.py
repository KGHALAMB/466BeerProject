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
import cleanData
from sklearn.tree import export_graphviz
from six import StringIO  
from IPython.display import Image  
import pydotplus


df = pd.read_csv('beer.csv')

df = cleanData.cleanAllData(df)
print(df.head())

print(df.good_beer.value_counts())

attributes = ['ABV', 'avg_IBU', 'Astringency', 'Body', 'Alcohol', 'Bitter', 'Sweet', 'Sour', 'Salty', 'Fruits', 'Hoppy', 'Spices', 'Malty']

#df = df[df['number_of_reviews'] > 10]

X = df[attributes]
y = df['good_beer']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=5)

clf = DecisionTreeClassifier()
clf = clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)
print("Accuracy:",metrics.accuracy_score(y_test, y_pred))


dot_data = StringIO()
export_graphviz(clf, out_file=dot_data,  
                filled=True, rounded=True,
                special_characters=True,feature_names = attributes, class_names=['Good', 'Okay', 'Bad'])
graph = pydotplus.graph_from_dot_data(dot_data.getvalue())  
graph.write_png('beer.png')
Image(graph.create_png())

