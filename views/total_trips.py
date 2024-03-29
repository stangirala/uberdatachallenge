# Globals defined in init
from __init__ import dbconn, ridesdb, ridescoll, clienttrip, keys, version

from flask import Flask, request, jsonify, abort, Blueprint
import json, time
from pymongo import Connection

total_trips = Blueprint('total_trips', __name__)

@total_trips.route('/'+version+'/total_trips.json', methods = ['GET'])
def get_total_trips():
    ''' Total trips recorded.
    Time is represented as seconds since unix epoch. '''
    result = {}
    trips = 0
    if request.json and ('start_time' and 'end_time' in request.json):
        records = ridescoll.find({"$and": [{'start_time': {"$gt": request.json['start_time']}},
                                           {'start_time': {"$lt": request.json['end_time']}}
                                          ]})
        trips = records.count()
    else:
        trips = ridescoll.count()

    result['total_trips'] = trips

    return jsonify(result), 200
