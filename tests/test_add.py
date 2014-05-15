import requests
import json, time, random

main_url = 'http://127.0.0.1:5000/'

def add_data():
    url = main_url + 'add.json'

    headers = {'content-type': 'application/json'}
    record = {}

    # Good data.
    record['client_id'] = 1011
    record['driver_id'] = 7432
    record['start_time'] = int(time.time())
    record['lat'] = 100
    record['lng'] = 200
    record['fare'] = 100
    record['rating'] = 3.5
    record['distance'] = 2

    for i in xrange(100):
        if i % 5== 0:
            record['client_id'] += 1
        if i % 6 == 0:
            record['driver_id'] += 1
        record['distance'] = random.uniform(1, 20)
        record['lat'] += 1
        record['lng'] += 1
        record['rating'] = random.uniform(1, 5)
        r = requests.post(url, data = json.dumps(record), headers=headers)
        assert r.status_code == 201

    # Bad data.
    record['client_id'] = -1
    record['driver_id'] = 7432
    record['start_time'] = 100
    record['lat'] = 100.1
    record['lng'] = 2
    record['fare'] = 15.07
    record['distance'] = 0
    record['rating'] = 3.5
    r = requests.post(url, data = json.dumps(record), headers=headers)
    assert r.status_code == 400

if __name__ == '__main__':
    add_data()
