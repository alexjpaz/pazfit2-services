import logging
log = logging.getLogger(__name__)

import math 
import json
from collections import OrderedDict

class Config(object):
	bar = 45
	bbb = 0.6
	plates = [45,35,25,10,5,2.5]
	week = {
		'3x5': [0.65,0.75,0.85],
		'3x3': [0.7,0.8,0.9],
		'531': [0.75,0.85,0.95],
		'DL': [0.4,0.5,0.6]
	}

config = {
	"bar": 45,
	"bbb": 0.6,
	"plates": [45,35,25,10,5,2.5],
	"num_plates": { # at home setup
		'45': 4,
		'35' : 4,
		'25' : 4,
		'10' : 4,
		'5'  : 8,
		'2.5': 4
	},
	"method": {
		"531": {
			'3x5': [0.65,0.75,0.85],
			'3x3': [0.7,0.8,0.9],
			'531': [0.75,0.85,0.95],
			'DL': [0.4,0.5,0.6]
		},
		"gzcl": {
			'X': [ i/1000.0 for i in range(400,1025,25) ]
		}
	}
}

class WeekTable(object):
	press=0
	deadlift=0
	bench=0
	squat=0

def parse_sides(param):
	sides = 2
	if '_1' in param: 
		sides = 1
		config["bar"] = 0

	return sides

def calculate_plates(weight=None, sides=2):
	oneside = []
	number_of_plates = 0

	weight = weight - config["bar"]

	for plate in config["plates"]:
		number_of_plates = math.floor((weight / plate) / sides)

		count = (config["num_plates"][str(plate)] / sides)

		# decrement weight
		if number_of_plates > count:
			actual_number_of_plates = count
		else:
			actual_number_of_plates = number_of_plates


		weight = (weight - (actual_number_of_plates*plate*sides))

		oneside.append(actual_number_of_plates)

	return oneside


def generate_month(maxes, method):
	month = OrderedDict()

	for mm in maxes:
		lift = mm[0]
		lift_max = int(mm[1])
		
		month[lift_max] = {}
		for week in config['method'][method].keys():
			month[lift_max][week] = generate_week(lift_max, week, method)

	return month

def generate_week(max_weight=0, week=None, method='531'):

	rows = OrderedDict()

	for fraction in config["method"][method][week]:
		weight = round(max_weight*fraction / 5) * 5;
		plates = calculate_plates(weight)
		plates.insert(0,weight)
		rows[fraction] = plates

	return rows

def goal(max_weight, weight):
	return int(round(37-36*weight/(max_weight+5)));

def get_pretty_print(json_object):
    return json.dumps(json_object, sort_keys=True, indent=4, separators=(',', ': '))
