# Globals defined in init
from __init__ import dbconn, ridesdb, ridescoll, clienttrip, keys, version

from flask import Flask, request, jsonify, abort, Blueprint
import json, time
from pymongo import Connection

trips_in_time_range = Blueprint('trips_in_time_range', __name__)

@trips_in_time_range.route('/'+version+'/trips_in_time_range.json', methods = ['GET'])
def get_trips_in_time_range():
    ''' Total number of trips in some time range. Default range is one hour.
    Function assumes inserts are not done in the future. If they are, then given
    and update function for distance and the fare should be specified in which case
    this method would have to be modified suitable.
    Time is represented as seconds since unix epoch. '''
    records = []
    if request.json and all (i in request.json for i in ('start_time', 'end_time')):
        collection = ridescoll.find({"$and": [{'start_time': {"$gt": request.json['start_time']}},
                                              {'start_time': {"$lt": request.json['end_time']}}
                                             ]})
    else:
        if request.json is None:
            collection = ridescoll.find({'start_time': {"$gt": int(time.time())-3600}})
        else:
            abort(400)

    for record in collection:
        del record['_id']
        records.append(record)

    result = {}
    result['trips'] = records

    return jsonify(result), 200
