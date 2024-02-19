import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score, accuracy_score, precision_score, \
    recall_score, f1_score
from sklearn.model_selection import train_test_split

from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline

df = pd.read_csv('beer.csv')
filtered_data = df[df['number_of_reviews'] > 50]

def help(x):
    if x > 4.5:
        return "Good"
    elif x > 3:
        return "Okay"
    else:
        return "Bad"

filtered_data["good_beer"] = filtered_data.apply(lambda x: help(x['review_overall']), axis=1)

attributes = ['ABV', 'Min IBU', 'Max IBU', 'Astringency', 'Body', 'Alcohol', 'Bitter', 'Sweet', 'Sour', 'Salty', 'Fruits', 'Hoppy', 'Spices', 'Malty']
X = filtered_data[attributes]
y = filtered_data['good_beer']


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=5)


scaler = StandardScaler()
mlp = MLPClassifier(solver='adam', alpha=1e-5, hidden_layer_sizes=(15,), random_state=1,  max_iter=1000)
#lbfgs is better for smaller datasets, but didn't work
pipeline = make_pipeline(scaler, mlp)

pipeline.fit(X_train, y_train)
predictions = pipeline.predict(X_test)

accuracy = accuracy_score(y_test, predictions)
precision = precision_score(y_test, predictions, average='weighted')
recall = recall_score(y_test, predictions, average='weighted')
f1 = f1_score(y_test, predictions, average='weighted')

print("Accuracy:", accuracy)
print("Precision:", precision)
print("Recall:", recall)
print("F1 Score:", f1)
