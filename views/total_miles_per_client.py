# Globals defined in init
from __init__ import dbconn, ridesdb, ridescoll, clienttrip, keys, version

from flask import Flask, request, jsonify, abort, Blueprint
import json, time
from pymongo import Connection

total_miles_per_client = Blueprint('/'+version+'total_miles_per_client', __name__)

'''Time is represented as seconds since unix epoch. '''
@total_miles_per_client.route('/'+version+'/total_miles_per_client.json', methods = ['GET'])
def get_total_miles_per_client():
    result = {}
    coll = clienttrip.find()

    if request.json and all (i in request.json for i in ('start_time', 'end_time')):
        for i in coll:
            total = 0
            records = ridescoll.find({"$and": [{'client_id': i['client_id']},
                                               {'start_time': {"$gt": request.json['start_time']}},
                                               {'start_time': {"$lt": request.json['end_time']}}
                                              ]})
            for record in records:
                total += record['distance']
            result[i['client_id']] = total
    elif request.json is None:
        for i in coll:
            result[i['client_id']] = i['distance']
    else:
        abort(400)

    return jsonify(result), 201
