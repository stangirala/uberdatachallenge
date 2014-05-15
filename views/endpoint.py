# Globals defined in init
from __init__ import dbconn, ridesdb, ridescoll, clienttrip, keys

from flask import Flask, request, jsonify, abort, Blueprint
import json, time
from pymongo import Connection

# View functions
from index import index
from add import add
from total_trips import total_trips
from unique_clients import unique_clients
from trips_in_time_range import trips_in_time_range
from total_miles_per_client import total_miles_per_client
from avg_city_fare import avg_city_fare
from median_driver_rating import median_driver_rating

# Flask globals
app = Flask(__name__)
app.register_blueprint(index)
app.register_blueprint(add)
app.register_blueprint(total_trips)
app.register_blueprint(unique_clients)
app.register_blueprint(trips_in_time_range)
app.register_blueprint(total_miles_per_client)
app.register_blueprint(avg_city_fare)
app.register_blueprint(median_driver_rating)

def run_app(host=None, port=None, debug=False):
    if host is None or port is None:
        app.run(debug = debug)
    else:
        app.run(host=host, port=port, debug=True)
