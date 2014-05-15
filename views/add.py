from __init__ import dbconn, ridesdb, ridescoll, clienttrip, keys, version

from flask import Flask, request, jsonify, abort, Blueprint
import json, time
from pymongo import Connection

add = Blueprint('add', __name__)

''' Returns request json object representing a sucessful insert.
Time is represented as seconds since unix epoch. '''
@add.route('/'+version+'/add.json', methods = ['POST'])
def record_trip_event():
    if not request.json:
        abort(400)
    else:
        for i in keys:
            if i not in request.json:
                abort(400)

        try:
            assert request.json['client_id'] is not None
            assert request.json['driver_id'] is not None
            assert request.json['start_time'] > 0
            assert request.json['lat'] > 0
            assert request.json['lng'] > 0
            assert request.json['fare'] > 0
            assert request.json['distance'] > 0
            assert request.json['rating'] > 0
        except AssertionError:
            abort(400)

        record = {}
        record['client_id'] = request.json['client_id']
        record['driver_id'] = request.json['driver_id']
        record['start_time'] = request.json['start_time']
        record['lat'] = request.json['lat']
        record['lng'] = request.json['lng']
        record['fare'] = request.json['fare']
        record['distance'] = request.json['distance']
        record['rating'] = request.json['rating']

        clienttripdata = {}
        clienttripdata['client_id'] = record['client_id']
        crecord = clienttrip.find({'client_id': record['client_id']})

        if crecord.count() == 0:
            clienttripdata['distance'] = record['distance']
            clienttrip.insert(clienttripdata)
        else:
            clienttrip.update({'client_id': record['client_id']},
                {"$set": {'distance':
                            crecord[0]['distance']+record['distance']}})

        ridescoll.insert(record)
        del record['_id']

        return jsonify(record), 201
