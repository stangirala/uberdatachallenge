# Globals defined in init
from __init__ import dbconn, ridesdb, ridescoll, clienttrip, keys, version

from flask import Flask, request, jsonify, abort, Blueprint
import json, time
from pymongo import Connection

unique_clients = Blueprint('unique_clients', __name__)

''' Total number of clients who have taken trips.
A client in the \'ridescollection\' indicates a trip taken.
Time is represented as seconds since unix epoch. '''
@unique_clients.route('/'+version+'/unique_clients.json', methods = ['GET'])
def get_total_clients_with_trips():
    result = {}
    count = 0
    if request.json and all (i in request.json for i in ('start_time', 'end_time')):
        records = ridescoll.find({"$and": [{'start_time': {"$gt": request.json['start_time']}},
                                           {'start_time': {"$lt": request.json['end_time']}}
                                          ]})
        count = len(records.distinct('client_id'))
    elif request.json is None:
        count = len(ridescoll.distinct('client_id'))
    else:
        abort(400)

    result['client_count'] = count

    return jsonify(result), 200
