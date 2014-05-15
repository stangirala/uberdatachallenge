import requests
import json, time, random

main_url = 'http://127.0.0.1:5000/'

def test_http():
    url = main_url

    headers = {'content-type': 'text'}

    data = ''
    r = requests.get(url, data=json.dumps(data), headers=headers)
    print r.text
    assert r.status_code == 200

    headers = {'content-type': 'text'}

    data = ''
    r = requests.post(url, data=json.dumps(data), headers=headers)
    assert r.status_code != 200

    headers = {'content-type': 'json'}
    data = ''
    r = requests.post(url, data=json.dumps(data), headers=headers)
    assert r.status_code == 405

if __name__ == '__main__':
    test_http()
