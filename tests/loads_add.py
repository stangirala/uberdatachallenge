import requests
import json, time, random
from loads.case import TestCase

main_url = 'http://127.0.0.1:5000/v1/'
url = main_url + 'add.json'

class TestAddEndpoint(TestCase):
    def test_add(self):
        headers = {'content-type': 'application/json'}
        record = {}

        record['client_id'] = 1011+random.uniform(0, 100)
        record['driver_id'] = 7432+random.uniform(0, 100)
        record['start_time'] = int(time.time())
        record['lat'] = 100+random.uniform(0, 100)
        record['lng'] = 200+random.uniform(0, 100)
        record['fare'] = 100
        record['rating'] = random.uniform(1, 5)
        record['distance'] = random.uniform(1, 10)

        res = self.session.post(url, data = json.dumps(record), headers=headers)
        self.assertEqual(res.status_code, 201)
