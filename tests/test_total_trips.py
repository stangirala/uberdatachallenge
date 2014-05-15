import requests
import json, time, random

main_url = 'http://127.0.0.1:5000/'

def total_trips(start_time=None, end_time=None):
    url = main_url+'total_trips.json'
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
    print '\n***Total Trips\n'
    total_trips()

    print '\n***Total Trips Valid Range\n'
    total_trips(1400115184, 1400121549)

    print '\n***Total Trips Pre-history\n'
    total_trips(0, 1000)

