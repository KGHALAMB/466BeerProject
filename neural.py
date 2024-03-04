import pandas as pd
import seaborn as sns
from sklearn.metrics import accuracy_score, precision_score, confusion_matrix, classification_report, recall_score, f1_score
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV
import matplotlib
matplotlib.use('TkAgg')  # Choose an appropriate backend, like TkAgg, Qt5Agg, etc.
import matplotlib.pyplot as plt

df = pd.read_csv('beer.csv')
filtered_data = df[df['number_of_reviews'] > 10]

def help(x):
    if x > 4.25: #use 4.4 because that gives 6 beers in y_test
        return "Good"
    elif x > 3:
        return "Okay"
    else:
        return "Bad"

filtered_data["good_beer"] = filtered_data.apply(lambda x: help(x['review_overall']), axis=1)

#filter and clean data. 80% train 20% test
attributes = ['ABV', 'Min IBU', 'Max IBU', 'Astringency', 'Body', 'Alcohol', 'Bitter', 'Sweet', 'Sour', 'Salty', 'Fruits', 'Hoppy', 'Spices', 'Malty']
X = filtered_data[attributes]
y = filtered_data['good_beer']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=5)


#standardize, model, fit, and predict
scaler = StandardScaler()
model = MLPClassifier(solver='adam', random_state=1, max_iter=1000) #lbfgs is better for smaller datasets, but didn't work
pipeline = make_pipeline(scaler, model) #model scaled
# pipeline = make_pipeline(model) #model not scaled

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


# Confusion Matrix
labels = ['Bad', "Okay", "Good"]
cm = confusion_matrix(y_test, predictions,  labels=labels)
print("Confusion Matrix:")
print(cm)

# Classification Report
print("\nClassification Report:")
print(classification_report(y_test, predictions))


#validation
print("here")
cv_scores = cross_val_score(pipeline, X, y, cv=5)  # You can adjust cv=5 to the number of desired folds
# cv_scores = cross_val_score(pipeline, X, y, cv=10)  # You can adjust cv=5 to the number of desired folds

print("Cross-validation Scores:", cv_scores)
print("Mean CV Accuracy:", cv_scores.mean())


# confusion matrix visual
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=["Bad", "Okay", "Good"], yticklabels=["Bad", "Okay", "Good"])
plt.xlabel("Predicted Label")
plt.ylabel("True Label")
plt.title("Confusion Matrix")
plt.show()