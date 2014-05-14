from flask import Flask, request, jsonify
import json
from pymongo import Connection

# Flask and DB globals
app = Flask(__name__)
dbconn = Connection('mongodb://localhost:27017/')

ridesdb = dbconn['ridesdb']
ridescoll = ridesdb['ridescollection']

keys = ['client_id', 'driver_id', 'lat', 'lng', 'fare',
    'distance', 'rating']

@app.route('/', methods = ['GET'])
def hello_word():
    if request.method == 'GET':
        return 'Hey there, try JSON!'
    else:
        abort(400)

''' Returns request json object representing a sucessful insert. '''
@app.route('/add.json', methods = ['POST'])
def add_transaction():
    if not request.json:
        abort(400)
    else:

        for i in keys:
            if i not in request.json:
                abort(400)

        assert request.json['client_id'] is not None
        assert request.json['driver_id'] is not None
        assert request.json['lat'] > 0
        assert request.json['lng'] > 0
        assert request.json['fare'] > 0
        assert request.json['distance'] > 0
        assert request.json['rating'] > 0

        record = {}
        record['client_id'] = request.json['client_id']
        record['driver_id'] = request.json['driver_id']
        record['start_time'] = request.json['start_time']
        record['lat'] = request.json['lat']
        record['lng'] = request.json['lng']
        record['fare'] = request.json['fare']
        record['distance'] = request.json['distance']
        record['rating'] = request.json['rating']

        ridescoll.insert(record)
        del record['_id']

        return jsonify(record), 201

def run_app(host=None, port=None):
    # DO argument checking.
    debug = True
    if host is None or port is None:
        app.run(debug = debug)
    else:
        app.run(host=host, port=port, debug=True)
