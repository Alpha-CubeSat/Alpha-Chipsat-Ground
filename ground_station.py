from elasticsearch import Elasticsearch
import requests
from time import sleep
from datetime import datetime, timezone
import pytz
from creds import elastic_auth

# Maps a value from 0-255 to a specified range
# def unmap_range(x, out_min, out_max):
#     return out_min + (((out_max - out_min) / 255) * x)

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

# fetch API every 30 seconds
while True:
    api = requests.get('https://api.tinygs.com/v2/packets?satellite=' + satellite_name).json()['packets']

    # iterates from most recent to oldest
    new_packets = 0
    for packet in api:
        # send packet to elasticsearch if it hasn't been processed yet
        payload = packet['parsed']['payload']
        packet_time = datetime.fromtimestamp(packet['serverTime']/1000, timezone.utc)
        if packet_time > last_processed_time:
            data = {
                "timestamp": packet_time.isoformat(),
                "chipsatId": payload['chipsatId'],
                "location": {
                    "lat": payload['latitude'],
                    "lon": payload['longitude'],
                },
                "altitude": payload['altitude'],
                "gyroX": payload['gyroX'],
                "gyroY": payload['gyroY'],
                "gyroZ": payload['gyroZ'],
                "accelX": payload['accelX'],
                "accelY": payload['accelY'],
                "accelZ": payload['accelZ'],
                "magX": payload['magX'],
                "magY": payload['magY'],
                "magZ": payload['magZ'],
                "temperature": payload['temperature'],
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

    sleep(30)
