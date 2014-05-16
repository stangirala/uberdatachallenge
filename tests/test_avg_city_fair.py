import requests
import json, time, random

main_url = 'http://127.0.0.1:5000/v1/'

def average_city_fare(lat1, lng1, lat2, lng2, start_time=None, end_time=None):
    url = main_url+'avg_city_fare.json'
    headers = {'content-type': 'application/json'}
    data = {}
    data['lat1'] = lat1
    data['lat2'] = lng1
    data['lng1'] = lat2
    data['lng2'] = lng2
    if (not (start_time is None)) and (not (end_time is None)):
        data['start_time']=start_time
        data['end_time']=end_time
    r = requests.get(url, data=json.dumps(data), headers=headers)
    print r.text
    return r.status_code

if __name__ == '__main__':
    print '***Average City Fare'
    assert average_city_fare(1, 220, 120, 230) == 200
    assert average_city_fare(300, 301, 400, 401) == 200

    print '***Average City Fare Time Range'
    assert average_city_fare(1, 220, 120, 230, 1, int(time.time())) == 200
