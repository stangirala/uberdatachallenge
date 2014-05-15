import requests
import json, time, random

main_url = 'http://127.0.0.1:5000/'

def get_median_driver_rating(driver_id, start_time=None, end_time=None):
    url = main_url+'median_drive_rating.json'
    headers = {'content-type': 'application/json'}
    data = {}
    if (not (start_time is None)) and (not (end_time is None)):
        data['start_time'] = start_time
        data['end_time'] = end_time
    data['driver_id'] = driver_id
    r = requests.get(url, data=json.dumps(data), headers=headers)
    print r.text
    assert r.status_code == 201

if __name__ == '__main__':
    print '***Median Driver Rating'
    get_median_driver_rating(7435)

    print '***Median Driver Rating Time Range'
    get_median_driver_rating(7435, 1, int(time.time()))
