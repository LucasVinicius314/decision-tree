import graphviz

from sklearn import tree
from sklearn.datasets import load_iris

# X = [[0, 0], [1, 1]]
# Y = [0, 1]

iris = load_iris()

x, y = iris.data, iris.target

clf = tree.DecisionTreeClassifier()

clf = clf.fit(x, y)

# clf.predict([[2., 2.]])

# tree.plot_tree(clf)

dot_data = tree.export_graphviz(clf, out_file=None) 

graph = graphviz.Source(dot_data) 
graph.render('output/iris')
