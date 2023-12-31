# -*- coding: utf-8 -*-
"""RFC.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1IsuQ4HghHvF1zpgoWNk2Ka0vsmoAYDKW
"""

from google.colab import drive
drive.mount('/content/gdrive')

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

dataset = pd.read_excel("/content/gdrive/MyDrive/FinancingData/DataClean10.xlsx")

"""# **Importing Libraries**"""

# Data Processing
import pandas as pd
import numpy as np

# Modelling Random Forest Classifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, precision_score, recall_score, ConfusionMatrixDisplay
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.model_selection import RandomizedSearchCV, train_test_split
from scipy.stats import randint

# Tree Visualisation
from sklearn.tree import export_graphviz
from IPython.display import Image
import graphviz

#making heatmap
plt.figure(figsize=(12, 6))
graph2 = sns.heatmap(dataset.corr(),
            cmap = 'BrBG',
            fmt = '.2f',
            linewidths = 2,
            annot=True)

"""# **Modelling**"""

# Split the data into features (X) and target (y)
X = dataset.drop('plafond_bin', axis=1)
y = dataset['plafond_bin']

# Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

#making the model
rf = RandomForestClassifier().fit(X_train, y_train)

#predict the model
y_pred = rf.predict(X_test)

"""# **Visualizing Results**"""

#print accuracy
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

# View confusion matrix for test data and predictions
cm = confusion_matrix(y_test, y_pred)

#Display Confusion Matrix
import seaborn
import matplotlib.pyplot as plt


def plot_confusion_matrix(data, labels, output_filename):
    """Plot confusion matrix using heatmap.

    Args:
        data (list of list): List of lists with confusion matrix data.
        labels (list): Labels which will be plotted across x and y axis.
        output_filename (str): Path to output file.

    """
    seaborn.set(color_codes=True)
    plt.figure(1, figsize=(9, 6))

    plt.title("Confusion Matrix")

    seaborn.set(font_scale=1.4)
    ax = seaborn.heatmap(data, annot=True, cmap="YlGnBu", cbar_kws={'label': 'Scale'})

    ax.set_xticklabels(labels)
    ax.set_yticklabels(labels)

    ax.set(ylabel="True Label", xlabel="Predicted Label")

    plt.savefig(output_filename, bbox_inches='tight', dpi=300)
    plt.close()

# define data
data = cm

# define labels
labels = ['500M - 1B', '1B-5B', '5B-10B', '10B - 30B/more']

# create confusion matrix
plot_confusion_matrix(data, labels, "confusion_matrix.png")

# Get and reshape confusion matrix data
matrix = confusion_matrix(y_test, y_pred)
matrix = matrix.astype('float') / matrix.sum(axis=1)[:, np.newaxis]

# Build the plot
plt.figure(figsize=(16,7))
sns.set(font_scale=1.4)
sns.heatmap(matrix, annot=True, annot_kws={'size':10},
            cmap=plt.cm.Greens, linewidths=0.2)

# Add labels to the plot
class_names = ['500M - 1B', '1B-5B', '5B-10B',
               '10B - 30B/more']
tick_marks = np.arange(len(class_names))
tick_marks2 = tick_marks + 0.5
plt.xticks(tick_marks, class_names, rotation=25)
plt.yticks(tick_marks2, class_names, rotation=0)
plt.xlabel('Predicted label')
plt.ylabel('True label')
plt.title('Confusion Matrix for Random Forest Model')
plt.show()

# View the classification report for test data and predictions
print(classification_report(y_test, y_pred))

#Export the first three decision trees from the forest
for i in range(3):
    tree = rf.estimators_[i]
    dot_data = export_graphviz(tree,
                               feature_names=X_train.columns,
                               filled=True,
                               max_depth=2,
                               impurity=False,
                               proportion=True)
    graph = graphviz.Source(dot_data)
    display(graph)

"""# **Tuning Parameters**"""

#tuning
param_dist = {'n_estimators': randint(50,500),
              'max_depth': randint(1,20)}

# Create a random forest classifier
rf2 = RandomForestClassifier()

# Use random search to find the best hyperparameters
rand_search = RandomizedSearchCV(rf2,
                                 param_distributions = param_dist,
                                 n_iter=5,
                                 cv=5)

# Fit the random search object to the data
rand_search.fit(X_train, y_train)

# Create a variable for the best model
best_rf = rand_search.best_estimator_

# Print the best hyperparameters
print('Best hyperparameters:',  rand_search.best_params_)

# Generate predictions with the best model
y_pred2 = best_rf.predict(X_test)

# Create the confusion matrix
cm2 = confusion_matrix(y_test, y_pred2)

# define data
data2 = cm2

# create confusion matrix
plot_confusion_matrix(data2, labels, "confusion_matrix2.png")

# Get and reshape confusion matrix data for tuning phase
matrix2 = confusion_matrix(y_test, y_pred2)
matrix2 = matrix2.astype('float') / matrix2.sum(axis=1)[:, np.newaxis]

# Build the plot
plt.figure(figsize=(16,7))
sns.set(font_scale=1.4)
sns.heatmap(matrix, annot=True, annot_kws={'size':10},
            cmap=plt.cm.Greens, linewidths=0.2)

# Add labels to the plot
class_names = ['500M - 1B', '1B-5B', '5B-10B',
               '10B - 30B/more']
tick_marks = np.arange(len(class_names))
tick_marks2 = tick_marks + 0.5
plt.xticks(tick_marks, class_names, rotation=25)
plt.yticks(tick_marks2, class_names, rotation=0)
plt.xlabel('Predicted label')
plt.ylabel('True label')
plt.title('Confusion Matrix for Random Forest Model After Tuning')
plt.show()

# View the classification report for test data and predictions after tuning
print(classification_report(y_test, y_pred2))

# Create a series containing feature importances from the model and feature names from the training data after tuning
feature_importances = pd.Series(best_rf.feature_importances_, index=X_train.columns).sort_values(ascending=False)

# Plot a simple bar chart
feature_importances.plot.bar();

"""# **Saving The Model**"""

#saving the model
import pickle
pickle_out = open("rfclassifier.pkl", mode = "wb")
pickle.dump(best_rf, pickle_out)
pickle_out.close()