import requests
import json, time, random

main_url = 'http://127.0.0.1:5000/'

def total_trips():
    url = main_url+'total_trips.json'
    headers = {'content-type': 'text'}
    r = requests.get(url, data=None, headers=headers)
    print r.text
    assert r.status_code == 201

def client_count():
    url = main_url+'unique_clients.json'
    headers = {'content-type': 'text'}
    r = requests.get(url, data=None, headers=headers)
    print r.text
    assert r.status_code == 201

def trips_last_hour():
    url = main_url+'trips_in_last_hour.json'
    headers = {'content-type': 'text'}
    r = requests.get(url, data=None, headers=headers)
    print r.text
    assert r.status_code == 201

def client_distance():
    url = main_url+'total_miles_per_client.json'
    headers = {'content-type': 'text'}
    r = requests.get(url, data=None, headers=headers)
    print r.text
    assert r.status_code == 201

def average_city_fare(lat1, lng1, lat2, lng2):
    url = main_url+'avg_city_fare.json'
    headers = {'content-type': 'application/json'}
    data = {}
    data['lat1'] = lat1
    data['lat2'] = lng1
    data['lng1'] = lat2
    data['lng2'] = lng2
    r = requests.get(url, data=json.dumps(data), headers=headers)
    print r.text
    assert r.status_code == 201

def get_median_driver_rating(driver_id):
    url = main_url+'median_drive_rating.json'
    headers = {'content-type': 'application/json'}
    data = {}
    data['driver_id'] = driver_id
    r = requests.get(url, data=json.dumps(data), headers=headers)
    print r.text
    assert r.status_code == 201

def bad_get_median_driver_rating(driver_id):
    url = main_url+'median_drive_rating.json'
    headers = {'content-type': 'application/json'}
    data = {}
    data['driver_id'] = driver_id
    r = requests.get(url, data=json.dumps(data), headers=headers)
    assert r.status_code == 400

if __name__ == '__main__':
    print '***Total Trips'
    total_trips()

    print '***Client Count'
    client_count()

    print '***Trips in last hours'
    trips_last_hour()

    print '***Client Distance'
    client_distance()

    print '***Average City Fare'
    average_city_fare(1, 220, 120, 230)
    average_city_fare(300, 301, 400, 401)

    print '***Median Driver Rating'
    get_median_driver_rating(7435)
    bad_get_median_driver_rating(0)
