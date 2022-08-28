import graphviz

from pandas import read_csv, get_dummies
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier, export_graphviz

def numetric_transform(data):
  for column in data:
    data[column] = data[column].astype(str)
    data[column] = LabelEncoder().fit_transform(data[column])
  
  return data.astype(float)

# Data input.
data = read_csv('input/main.csv', sep=',').drop('Exemplo', axis=1)

# Printing the data that will be worked on.
print(data.to_string)

# Numeric transformation.
one_hot_data = numetric_transform(data).drop('conc', axis=1)

# Map data into x and y.
x, y = one_hot_data, data['conc']

# Training the main classifier.
classifier = DecisionTreeClassifier(criterion='entropy')
classifier.fit(x, y)

# Exporting the main classifier's decision graph.
dot_data = export_graphviz(
  classifier,
  out_file=None,
  feature_names=list(one_hot_data.columns.values), class_names=y.unique()
) 
graph = graphviz.Source(dot_data)
graph.render('output/main')

###############

# Splitting data for partial training.
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.20)

# Training the test classifier.
classifier = DecisionTreeClassifier(criterion='entropy')
classifier.fit(x_train, y_train)

# Generating predictions.
y_pred = classifier.predict(x_test)

# Printing metrics.
print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))

# Exporting the test classifier's decision graph.
dot_data = export_graphviz(
  classifier,
  out_file=None,
  feature_names=list(one_hot_data.columns.values), class_names=y.unique()
) 
graph = graphviz.Source(dot_data)
graph.render('output/main-test')
