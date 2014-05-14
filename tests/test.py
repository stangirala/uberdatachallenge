import requests, json

main_url = 'http://127.0.0.1:5000/'

def test_http():
    url = main_url

    headers = {'content-type': 'text'}

    data = ''
    r = requests.get(url, data=json.dumps(data), headers=headers)
    assert r.status_code == 200

    headers = {'content-type': 'text'}

    data = ''
    r = requests.post(url, data=json.dumps(data), headers=headers)
    assert r.status_code != 200

    headers = {'content-type': 'json'}
    data = ''
    r = requests.post(url, data=json.dumps(data), headers=headers)
    assert r.status_code == 405

def add_data():
    url = main_url + 'add.json'

    headers = {'content-type': 'application/json'}

    record = {}
    record['client_id'] = 1001
    record['driver_id'] = 7432
    record['start_time'] = 100
    record['lat'] = 100.1
    record['lng'] = 200.1
    record['fare'] = 15.07
    record['distance'] = 2
    record['rating'] = 3.5
    r = requests.post(url, data = json.dumps(record), headers=headers)
    print r.text
    assert r.status_code == 201


if __name__ == '__main__':
    test_http()
    add_data()
