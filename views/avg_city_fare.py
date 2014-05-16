# Globals defined in init
from __init__ import dbconn, ridesdb, ridescoll, clienttrip, keys, version

from flask import Flask, request, jsonify, abort, Blueprint
import json, time
from pymongo import Connection

avg_city_fare = Blueprint('avg_city_fare', __name__)

''' Per city fare, city defined by a square.
Data keys are defined by (lat, lng) tuples, not on boundary.
It's easier to specify two coordinates than distance on a globe, I think.
Time is represented as seconds since unix epoch. '''
@avg_city_fare.route('/'+version+'/avg_city_fare.json', methods = ['GET'])
def get_average_city_fare():

    result = {}
    sum = 0
    if request.json and all (i in request.json for i in ('lat1', 'lng1', 'lat2', 'lng2')):
        try:
            assert (type(request.json['lat1']) is float or type(request.json['lat1'] is int)) and request.json['lat1'] > 0
            assert (type(request.json['lat2']) is float or type(request.json['lat2'] is int)) and request.json['lat2'] > 0
            assert (type(request.json['lng1']) is float or type(request.json['lng1'] is int)) and request.json['lng1'] > 0
            assert (type(request.json['lng2']) is float or type(request.json['lng2'] is int)) and request.json['lng2'] > 0
        except AssertionError:
            abort(400)

        if all (j in request.json for j in ('start_time', 'end_time')):
            try:
                assert type(request.json['start_time']) is int and request.json['start_time'] > 0
                assert type(request.json['end_time']) is int and request.json['end_time'] > 0
            except AssertionError:
                abort(400)
            records = ridescoll.find({"$and":
                                        [{'lat': {"$gt": request.json['lat1']}},
                                         {'lat': {"$lt": request.json['lat2']}},
                                         {'lng': {"$gt": request.json['lng1']}},
                                         {'lng': {"$lt": request.json['lng2']}},
                                         {'start_time': {"$gt": request.json['start_time']}},
                                         {'start_time': {"$lt": request.json['end_time']}}
                                        ]})
            result['start_time'] = request.json['start_time']
            result['end_time'] = request.json['end_time']
        else:
            records = ridescoll.find({"$and":
                                        [{'lat': {"$gt": request.json['lat1']}},
                                         {'lat': {"$lt": request.json['lat2']}},
                                         {'lng': {"$gt": request.json['lng1']}},
                                         {'lng': {"$lt": request.json['lng2']}}
                                        ]})
        for record in records:
            sum += record['fare']
    else:
        abort(400)

    result['lat1'] = request.json['lat1']
    result['lat2'] = request.json['lat2']
    result['lng1'] = request.json['lng1']
    result['lng2'] = request.json['lng2']
    result['average_fare'] = sum

    return jsonify(result), 200
