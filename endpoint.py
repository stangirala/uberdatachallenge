from flask import Flask, request, jsonify, abort
import json, time
from pymongo import Connection

# Flask and DB globals
app = Flask(__name__)
dbconn = Connection('mongodb://localhost:27017/')

ridesdb = dbconn['ridesdb']
ridescoll = ridesdb['ridescollection']
clienttrip = ridesdb['clienttripcollection']

keys = ['client_id', 'driver_id', 'lat', 'lng', 'fare',
    'distance', 'rating']

@app.route('/', methods = ['GET'])
def display_index():
    ''' Return docs? '''
    if request.method == 'GET':
        return 'Hey there, try JSON!'
    else:
        abort(400)

''' Returns request json object representing a sucessful insert.
Time is represented as seconds since unix epoch. '''
@app.route('/add.json', methods = ['POST'])
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

''' Total trips recorded. '''
@app.route('/total_trips.json', methods = ['GET'])
def get_total_trips():
    result = {}
    result['total_trips'] = ridescoll.count()
    return jsonify(result), 201

''' Total number of clients who have taken trips.
A client in the \'ridescollection\' indicates a trip taken.'''
@app.route('/unique_clients.json', methods = ['GET'])
def get_total_clients_with_trips():
    result = {}
    result['client_count'] = len(ridescoll.distinct('client_id'))
    return jsonify(result), 201

''' Total number of trips in the last hour. '''
@app.route('/trips_in_last_hour.json', methods = ['GET'])
def get_trips_in_last_hour():
    ctimel = int(time.time())-3600

    records = []

    for record in ridescoll.find({'start_time': {"$gt": ctimel}}):
        del record['_id']
        records.append(record)

    result = {}
    result['trips'] = records

    return jsonify(result), 201

@app.route('/total_miles_per_client.json', methods = ['GET'])
def get_total_miles_per_client():
    coll = clienttrip.find()
    result = {}
    for i in coll:
        result[i['client_id']] = i['distance']

    return jsonify(result), 201

''' Per city fare, city defined by a square.
Data keys are defined by (lat, lng) tuples, not on boundary'''
@app.route('/avg_city_fare.json', methods = ['GET'])
def get_average_city_fare():
    if not request.json:
        abort(400)

    try:
        assert request.json['lat1'] > 0
        assert request.json['lat2'] > 0
        assert request.json['lng1'] > 0
        assert request.json['lng2'] > 0
    except AssertionError:
        abort(400)

    records = ridescoll.find({"$and":
                              [{'lat': {"$gt": request.json['lat1']}},
                               {'lat': {"$lt": request.json['lat2']}},
                               {'lng': {"$gt": request.json['lng1']}},
                               {'lng': {"$lt": request.json['lng2']}}
                              ]})
    sum = 0
    for record in records:
        sum += record['fare']

    result = {}
    result['lat1'] = request.json['lat1']
    result['lat2'] = request.json['lat2']
    result['lng1'] = request.json['lng1']
    result['lng2'] = request.json['lng2']
    result['average_fare'] = sum

    return jsonify(result), 201

@app.route('/median_drive_rating.json', methods = ['GET'])
def get_median_driver_rating():
    if not request.json:
        abort(400)

    try:
        assert request.json['driver_id'] > 0
    except AssertionError:
        abort(400)

    result = {}
    result['drive_id'] = request.json['driver_id']
    records = ridescoll.find({'driver_id': request.json['driver_id']}).sort('rating', 1)
    if records.count() == 0:
        result['median_rating'] = -1
    elif records.count() % 2 == 0:
        result['median_rating'] = (records[records.count()/2]['rating']
                                  +records[(records.count()-1)/2]['rating'])/2
    else:
        result['median_rating'] = records[records.count()/2]['rating']

    return jsonify(result), 201

def run_app(host=None, port=None, debug=False):
    if host is None or port is None:
        app.run(debug = debug)
    else:
        app.run(host=host, port=port, debug=True)
