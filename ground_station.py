import base64
from datetime import datetime, timezone
from time import sleep

import pytz
import requests
from elasticsearch import Elasticsearch

from creds import elastic_auth

# Maps a value from 0-255 to a specified range
# def unmap_range(x, out_min, out_max):
#     return out_min + (((out_max - out_min) / 255) * x)

# Maps each ChipSat ID to its gyro bias in each axis (the reported gyro value when the chipsat was stationary)
gyro_bias_map = {
    0: {
        'x': -25.94,
        'y': 10.57,
        'z': -14.41,
    },
    1: {
        'x': -10.57,
        'y': 0.96,
        'z': -4.80,
    },
    2: {
        'x': -0.96,
        'y': 2.88,
        'z': -10.57,
    },
    3: {
        'x': -10.57,
        'y': -8.65,
        'z': -10.57,
    },
}

satellite_name = 'ChipSats'
# satellite_name = 'ChipSat_A'
index_name = 'chipsats'

es = Elasticsearch(["https://alphags.jonathanjma.com:443/elasticsearch"], basic_auth=elastic_auth)

# timestamp of last processed packet
est = pytz.timezone('America/New_York')
last_processed_time = datetime(2024, 10, 27, 0, 0, tzinfo=est)

# find the time of the last processed packet in elasticsearch
if index_name in es.indices.get_mapping().keys():
    response = es.search(index=index_name, size=1, sort=[{'timestamp': {'order': 'desc'}}])

    # checks to make sure index not empty
    if len(response['hits']['hits']) > 0:
        last_processed_time = datetime.fromisoformat(response['hits']['hits'][0]['_source']['timestamp'])
        print("Last packet time was: " + str(last_processed_time.astimezone(est)))
    else:
        print("Index is empty")
else:
    print("Index not found")

# fetch API loop
while True:
    # need user agent so we appear as a browser
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36 Edg/141.0.0.0"}
    api = requests.get("https://api.tinygs.com/v2/packets?satellite=" + satellite_name, headers=headers).json()
    
    # Packets key might not exist if there are no recent packets
    if 'packets' in api:
        api = api['packets']

        # iterates from most recent to oldest
        new_packets = 0
        for packet in api:
            # send packet to elasticsearch if it hasn't been processed yet
            payload = packet['parsed']['payload']
            packet_time = datetime.fromtimestamp(packet['serverTime']/1000, timezone.utc)
            if packet_time > last_processed_time:
                gyro_bias = gyro_bias_map[payload['chipsatId']]
                data = {
                    "timestamp": packet_time.isoformat(),
                    "tinygsPacketId": packet['id'],
                    "data": base64.b64decode(packet['raw']).hex(),
                    "chipsatId": payload['chipsatId'],
                    "location": {
                        "lat": payload['latitudeDeg'],
                        "lon": payload['longitudeDeg'],
                    },
                    "altitude": payload['altitudeM'],
                    "gyroX": payload['gyroXDps'] + gyro_bias['x'],
                    "gyroY": payload['gyroYDps'] + gyro_bias['y'],
                    "gyroZ": payload['gyroZDps'] + gyro_bias['z'],
                    "accelX": payload['accelXG'],
                    "accelY": payload['accelYG'],
                    "accelZ": payload['accelZG'],
                    "magX": payload['magXUt'],
                    "magY": payload['magYUt'],
                    "magZ": payload['magZUt'],
                    "temperature": payload['temperatureC'],
                    "gpsPositionValid": payload['gpsPositionValid'],
                    "gpsAltitudeValid": payload['gpsAltitudeValid'],
                    "imuValid": payload['imuValid'],
                    "gpsOn": payload['gpsOn'],
                    "listenFlag": payload['lFlag'],
                    "validUplinks": payload['validUplinks'],
                    "invalidUplinks": payload['invalidUplinks'],
                }
                es.index(index=index_name, body=data)
                new_packets += 1

        print(f'{new_packets} new packets were received')

        # update last processed packet time (first packet is the latest one)
        last_processed_time = datetime.fromtimestamp(api[0]['serverTime']/1000, timezone.utc)
        print("Last packet time was: " + str(last_processed_time.astimezone(est)))
    else:
        print("No packets found in API response")

    sleep(30)
