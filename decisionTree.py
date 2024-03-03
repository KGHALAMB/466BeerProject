import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn import metrics
import cleanData
from sklearn.tree import export_graphviz
from six import StringIO  
from IPython.display import Image  
import pydotplus


df = pd.read_csv('beer.csv')

df = cleanData.cleanAllData(df) # uses cleanData script to modify the csv to work for a decision tree

print(df.good_beer.value_counts())

attributes = [
    'ABV', 
    'avg_IBU', 
    'Astringency', 
    'Body', 
    'Alcohol', 
    'Bitter', 
    'Sweet', 
    'Sour', 
    'Salty', 
    'Fruits', 
    'Hoppy', 
    'Spices', 
    'Malty'
    ]  # These are the chosen Beer attributes that we decided to use for the decision tree

X = df[attributes] # X data is the attributes
y = df['good_beer'] # Y data is the overall rating of the beer

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=5) # doing an 80 / 20 test Training split

clf = DecisionTreeClassifier() 
clf = clf.fit(X_train, y_train) # fit training data to the decision tree object

y_pred = clf.predict(X_test)
print("Accuracy:",metrics.accuracy_score(y_test, y_pred)) # getting metrics for the model
print("Matrix\n:",metrics.confusion_matrix(y_test, y_pred))


# creating png image representation of the decision tree
dot_data = StringIO()
export_graphviz(clf, out_file=dot_data,  
                filled=True, rounded=True,
                special_characters=True,feature_names = attributes, class_names=['Good', 'Okay', 'Bad'])
graph = pydotplus.graph_from_dot_data(dot_data.getvalue())  
graph.write_png('beer.png')
Image(graph.create_png())

