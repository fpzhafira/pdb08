from pyspark.mllib.tree import DecisionTree, DecisionTreeModel
from pyspark import SparkConf, SparkContext
from flask import request, redirect
from flask import jsonify
from flask import Response
from flask import render_template
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField



import requests
import json
import socket

from app import app

#Array2an
places = ["Chelsea", "Hell's Kitchen", "Hudson Yards", "Lincoln Square", "Little Spain"
	, "Manhattan Valley", "Penn South", "Pomander Walk", "Riverside South", "Upper West Side", "Astor Row", "East Harlem"
	,"Hamilton Heights", "Harlem", "Hudson Heights", "Inwood", "Le Petit Senegal", "Manhattanville", "Marble Hill", 
	"Marcus Garvey Park", "Morningside Heights", "Sugar Hill", "Sylvan", "Washington Heights", "Lenox Hill", "Turtle Bay"]


longitude = ["40.7465004", "40.7637581", "40.7542652", "40.7738280", "40.737103"
	, "40.796989", "40.747027", "40.793961", "40.816212", "40.787011", "40.810300", "40.795740"
	,"40.825960", "40.811550", "40.853497", "40.867714", "40.802343", "41.030430", "40.876117",	"40.804430", "40.808956", 
	"40.827930", "43.196458", "40.841708", "40.766232", "40.754037"]

latitude = ["74.0013737", "73.9918181", "74.0031180", "73.9844722", "73.997955"
	, "73.969707", "73.997757", "73.973326", "73.962039", "73.975368", "73.941600", "73.938921"
	,"73.949608", "73.946477", "73.937452", "73.921202", "73.951093", "73.712680", "73.910263",	"73.943583", "73.962433", 
	"73.944065", "75.730463", "73.939355", "73.960231", "73.966841"]


@app.route('/', methods=['GET'])
@app.route('/index')
def index():
	conf = SparkConf().setAppName("TaxiWeb")
	# sc = SparkContext(conf=conf)
	#model = DecisionTreeModel.load(sc, "TugasAkhir/Model/decision_tree/decision_tree_v5")

	return render_template('index.html')


@app.route('/index-2')
def index2():
	# conf = SparkConf().setAppName("TaxiWeb")
	# sc = SparkContext(conf=conf)
	#model = DecisionTreeModel.load(sc, "TugasAkhir/Model/decision_tree/decision_tree_v5")

	return render_template('index-2.html')

@app.route('/predict')
def chart():

	return render_template('charts.html', places=places)

@app.route('/predict-result', methods = ['POST'])
def result():
	pickupLoc = request.form['pickup']
	dropoffLoc = request.form['dropoff']
	passenger = request.form['passenger']
	tip = request.form['tip']
	toll = request.form['toll']
	timestamp = request.form['timestamp']

	#hitung distance
	longitude = None
	for x in range(len(places)):
		if places[x] == pickupLoc:
			longitude = x
			print longitude

	
	pickupLoc = {'pickupLoc' : pickupLoc}
	dropoffLoc = {'dropoffLoc' : dropoffLoc}
	passenger = {'passenger' : passenger}
	tip = {'tip' : tip}
	toll = {'toll' : toll}
	timestamp = {'timestamp' : timestamp}


	# print("The dropoff location is " + dropoffLoc + ".")
	return render_template('prediction-result.html', pickupLoc=pickupLoc, dropoffLoc=dropoffLoc, passenger=passenger,
		 tip=tip, toll=toll, timestamp=timestamp)
	
@app.errorhandler(404)
def not_found(e):	
	return Response('{"detail": "The requested URL was not found on the server.  If you entered the URL manually please check your spelling and try again.", "status": "404", "title": "Not Found"}', status=404, mimetype='application/json')
	
if __name__ == "__main__":
	app.run(host="0.0.0.0", port=8080, debug=True)
