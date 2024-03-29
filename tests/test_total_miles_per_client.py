import requests
import json, time, random

main_url = 'http://127.0.0.1:5000/v1/'

def client_distance(start_time=None, end_time=None):
    url = main_url+'total_miles_per_client.json'
    data = {}
    if not start_time is None:
        headers = {'content-type': 'application/json'}
        data['start_time'] = start_time
        data['end_time'] = end_time
    else:
        headers = {'content-type': 'text'}

    r = requests.get(url, data=json.dumps(data), headers=headers)
    print r.text
    assert r.status_code == 200

if __name__ == '__main__':
    print '***Client Distance'
    client_distance()

    print '***Client Distance in Range'
    client_distance(0, 100)

    print '***Client Distance in Recent Range'
    client_distance(1400121540, 1400186055)
