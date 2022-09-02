import graphviz

from pandas import read_csv, get_dummies, DataFrame
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier, export_graphviz

labelEncoder = LabelEncoder()

def numeric_transform(data: DataFrame, columns: list[str]) -> DataFrame:
  for column in columns:
    data[column] = labelEncoder.fit_transform(data[column].astype(str))

  return data

# Data input.
data = read_csv('input/main.csv', sep=',').drop('Exemplo', axis=1)

# Printing the data that will be worked on.
print(data.to_string)

# Numeric transformation.
numeric_data = numeric_transform(
  data, 
  [
    'Alternativo', 
    'Bar',
    'Sex/Sab',
    'fome',
    'Chuva',
    'Res',
  ]
).drop('conc', axis=1)

treated_data = get_dummies(
  numeric_data, 
  [
    'Cliente',
    'Preço',
    'Tipo',
    'Tempo',
  ]
)

# Map data into x and y.
x, y = treated_data, data['conc']

# Training the main classifier.
classifier = DecisionTreeClassifier(criterion='entropy')
classifier.fit(x, y)

class_names = [
  'Sim',
  'Não',
]

# Exporting the main classifier's decision graph. 
graphviz.Source(
  export_graphviz(
    classifier,
    out_file=None,
    feature_names=list(treated_data.columns.values), 
  )
).render('output/main')

###############

# Splitting data for partial training.
x_train, x_test, y_train, y_test = train_test_split(
  x,
  y,
  test_size=0.20,
  random_state=0
)
# Printing the treated data that will be worked on.
print(x_train.to_string())

# Training the test classifier.
classifier = DecisionTreeClassifier(criterion='entropy')
classifier.fit(x_train, y_train)

# Generating predictions.
y_pred = classifier.predict(x_test)

# Printing metrics.
conf_matrix = confusion_matrix(y_test, y_pred)
classif_report = classification_report(y_test, y_pred)
acc_score = accuracy_score(y_test, y_pred)

true_negatives, false_positives, false_negatives, true_positives = conf_matrix.ravel()

a = true_negatives + false_positives
b = false_negatives + true_positives

true_negative_rate = str(true_negatives / a)
false_positive_rate = str(false_positives / a)
false_negative_rate = str(false_negatives / b)
true_positive_rate = str(true_positives / b)

print(
  '\nTrue positive rate: ' + true_positive_rate +
  '\nTrue negative rate: ' + true_negative_rate +
  '\nFalse positive rate: ' + false_positive_rate +
  '\nFalse negative rate: ' + false_negative_rate +
  '\nAccuracy score: ' + str(acc_score)
)

print('\nconfusion matrix')
print(conf_matrix)

print('\nclassification report')
print(classif_report)

# Exporting the test classifier's decision graph. 
graphviz.Source(
  export_graphviz(
    classifier,
    out_file=None,
    feature_names=list(treated_data.columns.values), 
  )
).render('output/main-test')
