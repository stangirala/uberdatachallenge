import requests
import json, time, random
from loads.case import TestCase

# ../packages/bin/loads-runner loads_unique_clients.TestCountEndpoint.test_count -u 1000 --hits 10

main_url = 'http://127.0.0.1:5000/v1/'
url = main_url+'unique_clients.json'

class TestCountEndpoint(TestCase):
    def test_count(self):
        data = {}
        headers = {'content-type': 'text'}
        res = self.session.get(url, data=json.dumps(data), headers=headers)
        self.assertEqual(res.status_code, 200)

    def test_count_range(self):
        data = {}
        headers = {'content-type': 'application/json'}
        data['start_time'] = 0
        data['end_time'] = 100
        res = self.session.get(url, data=json.dumps(data), headers=headers)
        self.assertEqual(res.status_code, 200)
