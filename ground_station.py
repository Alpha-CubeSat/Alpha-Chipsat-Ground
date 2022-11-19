from elasticsearch import Elasticsearch
import requests
from time import sleep
from datetime import datetime
import pytz
from creds import elastic_auth

# use random satellite for testing purposes
satellite_name = 'SATLLA-2B' # 'Norbi'
index_name = 'satlla-2b'

# convert unix time to human-readable time
def convert_timestamp(unix_time_millis):
    return datetime.utcfromtimestamp(int(unix_time_millis)/1000).astimezone(pytz.timezone('America/New_York')).strftime("%Y-%m-%d %H:%M:%S")

es = Elasticsearch('https://localhost:9200')
# es = Elasticsearch('https://localhost:9200', basic_auth=elastic_auth, ca_certs='http_ca.crt')

# timestamp of last processed packet
last_processed_time = 0

# if index not found, create index
# else find the time of the last processed packet in elasticsearch
if index_name not in es.indices.get_mapping().keys():
    mappings = {
        'properties': {
            'serverTime': {'type': 'date'},
            'satelliteName': {'type': 'text'},
            'batteryVolts': {'type': 'double'},
            'batteryCurrent': {'type': 'double'},
            'power': {'type': 'double'},
            'temperature': {'type': 'double'},
            'position': {'type': 'geo_point'},
            'altitude': {'type': 'double'}
        }
    }

    es.indices.create(index=index_name, mappings=mappings)

    print(f"Created index '{index_name}'")
else:
    print(f"Found index '{index_name}'")

    response = es.search(index=index_name, size=1, sort=[
        {
            'serverTime': {
                'order': 'desc'
            }
        }
    ])
    hits = response['hits']['hits']

    # checks to make sure index not empty
    if len(hits) > 0:
        last_processed_time = response['hits']['hits'][0]['_source']['serverTime']
        print(f'Last packet time was: {last_processed_time} ({convert_timestamp(last_processed_time)})')
    else:
        print(f"Index '{index_name}' was empty")

# every 3 minutes, fetch api
while True:
    api = requests.get('https://api.tinygs.com/v2/packets?satellite=' + satellite_name).json()['packets']

    # iterates from most recent to oldest
    new_packets = 0
    for packet in api:

        # send packet to elasticsearch if it hasn't been processed yet
        if packet['serverTime'] > last_processed_time:
            data = {
                'serverTime': packet['serverTime'],
                'satelliteName': packet['satellite'],
                'batteryVolts': packet['parsed']['payload']['batteryVolts'],
                'batteryCurrent': packet['parsed']['payload']['batteryCurrent'],
                'power': packet['parsed']['payload']['tinygsTxPower'],
                'temperature': packet['parsed']['payload']['tinygsTemp'],
                'position': f"{packet['satPos']['lat']},{packet['satPos']['lng']}",
                'altitude': packet['satPos']['alt']
            }
            es.index(index=index_name, document=data)
            new_packets += 1

    print(f'{new_packets} new packets were received')

    # update last processed packet time (first packet is the latest one)
    last_processed_time = api[0]['serverTime']
    print(f'Last packet time: {last_processed_time} ({convert_timestamp(last_processed_time)})')

    sleep(180)
