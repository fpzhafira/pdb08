from flask import Flask
from flask import request
from flask import jsonify
from flask import Response
from flask import render_template

from pyspark.mllib.tree import DecisionTree, DecisionTreeModel
from pyspark import SparkConf, SparkContext

import requests
import json
import socket

app = Flask(__name__)
from app import views