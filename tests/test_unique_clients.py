import requests
import json, time, random

main_url = 'http://127.0.0.1:5000/v1/'

def client_count(start_time=None, end_time=None):
    url = main_url+'unique_clients.json'
    data = {}
    if (not (start_time is None)) and (not (end_time is None)):
        headers = {'content-type': 'application/json'}
        data['start_time'] = start_time
        data['end_time'] = end_time
    else:
        headers = {'content-type': 'text'}

    r = requests.get(url, data=json.dumps(data), headers=headers)
    print r.text
    assert r.status_code == 200

if __name__ == '__main__':
    print '***Client Count'
    client_count()

    print '***Client Count in Range'
    client_count(0, 100)
