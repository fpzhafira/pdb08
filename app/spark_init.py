from pyspark.mllib.tree import DecisionTree, DecisionTreeModel
from pyspark import SparkConf, SparkContext

conf = SparkConf().setAppName("TaxiWeb")
sc = SparkContext(conf=conf)
model = DecisionTreeModel.load(sc, "TugasAkhir/Model/decision_tree/decision_tree_v5")