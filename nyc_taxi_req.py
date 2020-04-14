import requests
import json
import time

def save_png(hex_str, file_name):
    import base64
    binary_string = base64.b64decode(hex_str)
    with open(file_name, 'wb') as png:
        png.write(binary_string)

def post_request(name, url, save, headers):
    with open('json/' + name + '.json') as f:
        data = json.load(f)

    start_time = time.time()
    r = requests.post(url=url, json=data, headers=headers)
    print("--- %s seconds ---" % (time.time() - start_time))
    print(r.text)

    if save:
        hex_str = r.json()['data']['result']
        save_png(hex_str, '/tmp/' + name + '.png')
    return r

def get_db_info(url_prefix, id, headers):
    url = url_prefix + '/db/table/info'
    r = requests.post(url=url, json={"id": id, "table": "nyc_taxi"}, headers=headers)
    print(r.text)

def login(url_prefix):
    url = url_prefix + '/login'
    r = requests.post(url=url, json={"username": "zilliz", "password": "123456"})
    print(r.json())
    token = r.json()['data']['token']
    return token

def get_db_id(url_prefix, headers):
    url = url_prefix + '/dbs'
    r = requests.get(url=url, headers=headers)
    print(r.json())
    id = str(r.json()['data'][0]['id'])
    return id

def run_sql(url_prefix, headers, json):
    url = url_prefix + '/db/query'
    r = requests.post(url=url, json=json, headers=headers)
    print(r.text)

if __name__ == "__main__":
    # sheep:
    url_prefix = 'http://192.168.2.26:8080'
    # AnZhen:
    # url_prefix = 'http://192.168.1.169:5555'

    token = login(url_prefix=url_prefix)
    headers = {"Authorization": "Token " + token}
    id = get_db_id(url_prefix=url_prefix, headers=headers)
    get_db_info(url_prefix=url_prefix, id=id, headers=headers)

    run_sql(url_prefix=url_prefix, headers=headers, json={'id': id, 'query': {'type': 'sql', 'sql': 'select count(*) from nyc_taxi'}})
    run_sql(url_prefix=url_prefix, headers=headers, json={'id': id, 'query': {'sql': 'SELECT count(*) AS countval FROM nyc_taxi', 'type': 'sql'}})
    run_sql(url_prefix=url_prefix, headers=headers, json={'id': id, 'query': {'type': 'sql', 'sql': 'SELECT MIN(fare_amount) as min , MAX(fare_amount) as max FROM nyc_taxi'}})
    run_sql(url_prefix=url_prefix, headers=headers, json={'id': id, 'query': {'sql': "SELECT ST_Point (dropoff_longitude, dropoff_latitude) AS point, avg(fare_amount) AS w FROM nyc_taxi WHERE (ST_Within (ST_Point (dropoff_longitude, dropoff_latitude), ST_GeomFromText('POLYGON ((-73.5 40.1, -73.5 41.1, -70.5 41.1, -70.5 40.1, -73.5 40.1))'))) GROUP BY point", 'type': 'heat', 'params': {'width': 810, 'height': 465, 'heat': {'bounding_box': [-73.5, 40.1, -70.5, 41.1], 'coordinate_system': 'EPSG:4326', 'map_zoom_level': 4, 'aggregation_type': 'avg'}}}})
    run_sql(url_prefix=url_prefix, headers=headers, json={'id': id, 'query': {'type': 'sql', 'sql': 'SELECT dropoff_longitude, dropoff_latitude FROM nyc_taxi WHERE dropoff_longitude IS NOT NULL AND dropoff_latitude IS NOT NULL LIMIT 1'}})
    run_sql(url_prefix=url_prefix, headers=headers, json={'id': id, 'query': {'sql': "SELECT ST_Point (dropoff_longitude, dropoff_latitude) AS point, avg(fare_amount) AS w FROM nyc_taxi WHERE (ST_Within (ST_Point (dropoff_longitude, dropoff_latitude), ST_GeomFromText('POLYGON ((-82.73103190893681 29.40507162320695, -82.73103190893681 50.36222793457449, -65.15290690893714 50.36222793457449, -65.15290690893714 29.40507162320695, -82.73103190893681 29.40507162320695))'))) GROUP BY point", 'type': 'heat', 'params': {'width': 400, 'height': 630, 'heat': {'bounding_box': [-82.73103190893681, 29.40507162320695, -65.15290690893714, 50.36222793457449], 'coordinate_system': 'EPSG:4326', 'map_zoom_level': 4, 'aggregation_type': 'avg'}}}})
    # run_sql(url_prefix=url_prefix, headers=headers, json={'id': id, 'query': {'sql': "SELECT ST_Point (dropoff_longitude, dropoff_latitude) AS point, avg(fare_amount) AS w FROM nyc_taxi WHERE (ST_Within (ST_Point (dropoff_longitude, dropoff_latitude), ST_GeomFromText('POLYGON ((-179.89999999999978 -26.400509849772284, -179.89999999999978 81.74354709384872, -66.8854430000034 81.74354709384872, -66.8854430000034 -26.400509849772284, -179.89999999999978 -26.400509849772284))'))) GROUP BY point", 'type': 'heat', 'params': {'width': 400, 'height': 630, 'heat': {'bounding_box': [-179.89999999999978, -26.400509849772284, -66.8854430000034, 81.74354709384872], 'coordinate_system': 'EPSG:4326', 'map_zoom_level': 1.3153444833432348, 'aggregation_type': 'avg'}}}})
