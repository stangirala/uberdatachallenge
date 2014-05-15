from pymongo import Connection

# DB globals
dbconn = Connection('mongodb://localhost:27017/')
ridesdb = dbconn['ridesdb']
ridescoll = ridesdb['ridescollection']
clienttrip = ridesdb['clienttripcollection']

keys = ['client_id', 'driver_id', 'start_time', 'lat', 'lng', 'fare',
        'distance', 'rating']
