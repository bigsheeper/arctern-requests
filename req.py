import requests
import json
import time

def save_png(hex_str, file_name):
    import base64
    binary_string = base64.b64decode(hex_str)
    with open(file_name, 'wb') as png:
        png.write(binary_string)

def post_request(name, url, save):
    with open('json/' + name + '.json') as f:
        data = json.load(f)

    start_time = time.time()
    r = requests.post(url=url, json=data)
    print("--- %s seconds ---" % (time.time() - start_time))

    if save:
        hex_str = r.json()['data']['result']
        save_png(hex_str, '/tmp/' + name + '.png')
    return r

def run_simple_test(url):
    post_request('point_map', url, True)
    # post_request('weighted_point_map', url, True)
    post_request('heat_map', url, True)
    post_request('choropleth_map', url, True)
    post_request('sql', url, False)

def run_pressure_test(url):
    for i in range(24 * 60):
        post_request('point_map', url, False)
        time.sleep(60)

if __name__ == "__main__":
    url = 'http://192.168.2.26:8080/db/query'
    # run_simple_test(url=url)
    run_pressure_test(url=url)
