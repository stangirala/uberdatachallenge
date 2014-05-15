# Globals defined in init
from __init__ import dbconn, ridesdb, ridescoll, clienttrip, keys

from flask import Flask, request, jsonify, abort, Blueprint
import json, time
from pymongo import Connection

median_driver_rating = Blueprint('median_driver_rating', __name__)

@median_driver_rating.route('/median_drive_rating.json', methods = ['GET'])
def get_median_driver_rating():
    if 'driver_id' in request.json:
        try:
            assert type(request.json['driver_id']) is int
        except AssertionError:
            abort(400)
        result = {}
        result['drive_id'] = request.json['driver_id']

        if all (i in request.json for i in ('start_time', 'end_time')):
            try:
                assert type(request.json['start_time']) is int
                assert type(request.json['end_time']) is int
            except AssertionError:
                abort(400)

            records = ridescoll.find({"$and": [{'driver_id': request.json['driver_id']},
                                               {'start_time': {"$gt": request.json['start_time']}},
                                               {'end_time': {"$lt": request.json['end_time']}}
                                              ]
                                    }).sort('rating', 1)
        else:
            records = ridescoll.find({'driver_id': request.json['driver_id']}).sort('rating', 1)

        if records.count() == 0:
            result['median_rating'] = -1
        elif records.count() % 2 == 0:
            result['median_rating'] = (records[records.count()/2]['rating']
                                       +records[(records.count()-1)/2]['rating'])/2
        else:
            result['median_rating'] = records[records.count()/2]['rating']
    else:
        abort(400)

    return jsonify(result), 201
