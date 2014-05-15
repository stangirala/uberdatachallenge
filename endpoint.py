from flask import Flask, request, jsonify, abort
import json, time
from pymongo import Connection

# Flask and DB globals
app = Flask(__name__)
dbconn = Connection('mongodb://localhost:27017/')

ridesdb = dbconn['ridesdb']
ridescoll = ridesdb['ridescollection']
clienttrip = ridesdb['clienttripcollection']

keys = ['client_id', 'driver_id', 'start_time', 'lat', 'lng', 'fare',
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

''' Total trips recorded.
Time is represented as seconds since unix epoch. '''
@app.route('/total_trips.json', methods = ['GET'])
def get_total_trips():
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

    return jsonify(result), 201

''' Total number of clients who have taken trips.
A client in the \'ridescollection\' indicates a trip taken.
Time is represented as seconds since unix epoch. '''
@app.route('/unique_clients.json', methods = ['GET'])
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

    return jsonify(result), 201

''' Total number of trips in some time range. Default range is one hour.
Function assumes inserts are not done in the future. If they are, then given
and update function for distance and the fare should be specified in which case
this method would have to be modified suitable.
Time is represented as seconds since unix epoch. '''
@app.route('/trips_in_time_range.json', methods = ['GET'])
def get_trips_in_time_range():
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

    return jsonify(result), 201

'''Time is represented as seconds since unix epoch. '''
@app.route('/total_miles_per_client.json', methods = ['GET'])
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

''' Per city fare, city defined by a square.
Data keys are defined by (lat, lng) tuples, not on boundary.
It's easier to specify two coordinates than distance on a globe, I think.
Time is represented as seconds since unix epoch. '''
@app.route('/avg_city_fare.json', methods = ['GET'])
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
            print 'SIX ARGS'
            print '*****start_time type', type(request.json['start_time'])
            try:
                assert type(request.json['start_time']) is int and request.json['start_time'] > 0
                assert type(request.json['end_time']) is int and request.json['end_time'] > 0
            except AssertionError:
                print 'ABORT SIZE ARGS'
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
            print 'COMPUTE FOUR ARGS'
            records = ridescoll.find({"$and":
                                        [{'lat': {"$gt": request.json['lat1']}},
                                         {'lat': {"$lt": request.json['lat2']}},
                                         {'lng': {"$gt": request.json['lng1']}},
                                         {'lng': {"$lt": request.json['lng2']}}
                                        ]})
        for record in records:
            sum += record['fare']
    else:
        print 'ABORT FOUR ARGS'
        abort(400)

    result['lat1'] = request.json['lat1']
    result['lat2'] = request.json['lat2']
    result['lng1'] = request.json['lng1']
    result['lng2'] = request.json['lng2']
    result['average_fare'] = sum

    return jsonify(result), 201

@app.route('/median_drive_rating.json', methods = ['GET'])
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

def run_app(host=None, port=None, debug=False):
    if host is None or port is None:
        app.run(debug = debug)
    else:
        app.run(host=host, port=port, debug=True)
