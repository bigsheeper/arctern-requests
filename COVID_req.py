import requests
import json

def save_png(hex_str, file_name):
    import base64
    binary_string = base64.b64decode(hex_str)
    with open(file_name, 'wb') as png:
        png.write(binary_string)

def get_db_info(url_prefix, id, headers):
    url = url_prefix + '/db/table/info'
    r = requests.post(url=url, json={"id": id, "table": "world_with_city"}, headers=headers)
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

def run_sql(url_prefix, save, headers, json):
    url = url_prefix + '/db/query'
    r = requests.post(url=url, json=json, headers=headers)
    print(r.text)

    if save:
        hex_str = r.json()['data']['result']
        save_png(hex_str, '/tmp/offscreen.png')
    return r

if __name__ == "__main__":
    # sheep:
    # url_prefix = 'http://192.168.2.26:8080'
    # AnZhen:
    url_prefix = 'http://192.168.1.169:5555'

    token = login(url_prefix=url_prefix)
    headers = {"Authorization": "Token " + token}
    id = get_db_id(url_prefix=url_prefix, headers=headers)
    get_db_info(url_prefix=url_prefix, id=id, headers=headers)

    run_sql(url_prefix=url_prefix, save=False, headers=headers, json={'id': id, 'query': {'type': 'sql', 'sql': 'select count(*) from world_with_city'}})
    run_sql(url_prefix=url_prefix, save=False, headers=headers, json={'id': id, 'query': {'type': 'sql', 'sql': "select ST_Point(Longitude, Latitude) as point, ConfirmedCount as s from world_with_city where LastUpdate like '%03-29%'"}})
    run_sql(url_prefix=url_prefix, save=False, headers=headers, json={"id": id, "query": {"sql": "select ST_Point(Longitude, Latitude) as point, ConfirmedCount as s from world_with_city where LastUpdate like '%03-29%'", "type": "weighted", "params": {"width": 938, "height": 1139, "weighted": {"opacity": 0.5, "bounding_box": [-74.03593615048472, 40.69688991687815, -73.8987365653707, 40.82319152940477], "coordinate_system": "EPSG:4326", "size_bound": [3], "color_bound": [6, 60], "color_gradient": ["#115f9a", "#d0f400"]}}}})
    run_sql(url_prefix=url_prefix, save=False, headers=headers, json={'id': id, 'query': {'sql': "SELECT ST_Point (dropoff_longitude, dropoff_latitude) AS point, avg(fare_amount) AS w FROM nyc_taxi WHERE (ST_Within (ST_Point (dropoff_longitude, dropoff_latitude), ST_GeomFromText('POLYGON ((-82.73103190893681 29.40507162320695, -82.73103190893681 50.36222793457449, -65.15290690893714 50.36222793457449, -65.15290690893714 29.40507162320695, -82.73103190893681 29.40507162320695))'))) GROUP BY point", 'type': 'heat', 'params': {'width': 400, 'height': 630, 'heat': {'bounding_box': [-82.73103190893681, 29.40507162320695, -65.15290690893714, 50.36222793457449], 'coordinate_system': 'EPSG:4326', 'map_zoom_level': 4, 'aggregation_type': 'avg'}}}})
