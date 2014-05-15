import requests
import json, time, random

main_url = 'http://127.0.0.1:5000/v1/'

def trips_in_time_range(start_time=None, end_time=None):
    url = main_url+'trips_in_time_range.json'
    data = {}
    if (not (start_time is None)) and (not (end_time is None)):
        headers = {'content-type': 'application/json'}
        data['start_time'] = start_time
        data['end_time'] = end_time
    else:
        headers = {'content-type': 'text'}

    r = requests.get(url, data=json.dumps(data), headers=headers)
    print r.text
    assert r.status_code == 201

if __name__ == '__main__':
    print '***Trips in last hour'
    trips_in_time_range()

    print '***Trips in range'
    trips_in_time_range(1, int(time.time()))
