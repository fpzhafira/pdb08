from pyspark.mllib.tree import DecisionTree, DecisionTreeModel
from pyspark import SparkConf, SparkContext
from flask import request, redirect
from flask import jsonify
from flask import Response
from flask import render_template
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from math import sin, cos, sqrt, atan2, radians



import requests
import json
import socket

from app import app

#Array2an
places = ["Chelsea", "Hell's Kitchen", "Hudson Yards", "Lincoln Square", "Little Spain"
	, "Manhattan Valley", "Penn South", "Pomander Walk", "Riverside South", "Upper West Side", "Astor Row", "East Harlem"
	,"Hamilton Heights", "Harlem", "Hudson Heights", "Inwood", "Le Petit Senegal", "Manhattanville", "Marble Hill", 
	"Marcus Garvey Park", "Morningside Heights", "Sugar Hill", "Sylvan", "Washington Heights", "Lenox Hill", "Turtle Bay"]


latitude = ["40.7465004", "40.7637581", "40.7542652", "40.7738280", "40.737103"
	, "40.796989", "40.747027", "40.793961", "40.816212", "40.787011", "40.810300", "40.795740"
	,"40.825960", "40.811550", "40.853497", "40.867714", "40.802343", "41.030430", "40.876117",	"40.804430", "40.808956", 
	"40.827930", "43.196458", "40.841708", "40.766232", "40.754037"]

longitude = ["74.0013737", "73.9918181", "74.0031180", "73.9844722", "73.997955"
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
	tip = float(request.form['tip'])
	toll = request.form['toll']
	timestamp = request.form['timestamp']

	#hitung toll amt
	tollAmt = None
	if toll == 'yes':
		tollAmt = float(5)
	else:
		tollAmt = float(0)

	#hitung extra fare
	(h, m) = timestamp.split(':')
	extraFare = 0
	h = int(h)
	if (6 <= h <= 8) or (16 <= h <= 18) or (0 <= h <= 4):
		extraFare = format(1, '.2f')

	


	#hitung distance
	longitude_var = None
	for x in range(len(places)):
		if places[x] == pickupLoc:
			longitude_var = float(longitude[x])
	
	latitude_var = None
	for x in range(len(places)):
		if places[x] == pickupLoc:
			latitude_var = float(latitude[x])

	longitude_var1 = None
	for x in range(len(places)):
		if places[x] == dropoffLoc:
			longitude_var1 = float(longitude[x])
	
	latitude_var1 = None
	for x in range(len(places)):
		if places[x] == dropoffLoc:
			latitude_var1 = float(latitude[x])

		# approximate radius of earth in km
	R = 6373.0

	lat1 = radians(latitude_var)
	lon1 = radians(longitude_var)
	lat2 = radians(latitude_var1)
	lon2 = radians(longitude_var1)

	dlon = lon2 - lon1
	dlat = lat2 - lat1

	a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
	c = 2 * atan2(sqrt(a), sqrt(1 - a))

	distance = format(R * c, '.2f')

	#itung fare amount
	farePerMile = float( R * c / 2.4)
	print(farePerMile)
	fare = format(2.5 + 0.4 * farePerMile, '.2f')
	print(fare)

	#hitung tax
	tax = float((2.5 + 0.4 * farePerMile) * 0.1)
	tax = format(tax, '.2f')
	
	totalAmt = float(float(fare) + float(extraFare) + float(tip) + float(tollAmt) + float(tax))
	
	prediksi = None
	if totalAmt > 5:
		prediksi = "Credit Card"
	else:
		prediksi = "Cash"

	pickupLoc = {'pickupLoc' : pickupLoc}
	dropoffLoc = {'dropoffLoc' : dropoffLoc}
	passenger = {'passenger' : passenger}
	tip = {'tip' : tip}
	tollAmt = {'tollAmt' : tollAmt}
	timestamp = {'timestamp' : timestamp}
	distance = {'distance' : distance}

	fare = {'fare' : fare}
	extraFare = {'extraFare' : extraFare}
	tax = {'tax' : tax}
	totalAmt = {'totalAmt' : totalAmt}
	prediksi = {'prediksi' : prediksi}


	# print("The dropoff location is " + dropoffLoc + ".")
	return render_template('prediction-result.html', pickupLoc=pickupLoc, dropoffLoc=dropoffLoc, passenger=passenger,
		 tip=tip, tollAmt=tollAmt, timestamp=timestamp, distance=distance, fare=fare, extraFare=extraFare, tax=tax, totalAmt=totalAmt, prediksi=prediksi)
	
@app.errorhandler(404)
def not_found(e):	
	return Response('{"detail": "The requested URL was not found on the server.  If you entered the URL manually please check your spelling and try again.", "status": "404", "title": "Not Found"}', status=404, mimetype='application/json')
	
if __name__ == "__main__":
	app.run(host="0.0.0.0", port=8080, debug=True)
