from elasticsearch import Elasticsearch
import requests
from time import sleep
from creds import elastic_auth

'''
1. connect to elasticsearch
2. create index if it does not exist
3. every 3 minutes, 
    fetch packet api for satellite
    send new packets to elasticsearch
'''

index_name = 'satlla-2b'

es = Elasticsearch("https://localhost:9200", basic_auth=elastic_auth, ca_certs='http_ca.crt')
if index_name not in es.indices.get_alias().keys():
    mappings = {
        "properties": {
            "serverTime": {"type": "date"},
            "satelliteName": {"type": "text"},
            "batteryVolts": {"type": "double"},
            "batteryCurrent": {"type": "double"},
            "power": {"type": "double"},
            "temperature": {"type": "double"},
            "position": {"type": "geo_point"},
            "altitude": {"type": "double"}
        }
    }

    es.indices.create(index=index_name, mappings=mappings)

    print('Created index ' + index_name)
else:
    print('Found index ' + index_name)

last_processed_time = 0

while True:
    # https://api.tinygs.com/v2/packets?satellite=Norbi
    api = requests.get('https://api.tinygs.com/v2/packets?satellite=SATLLA-2B').json()['packets']
    print(api[0])

    # iterates from most recent to oldest
    new_packets = 0
    for packet in api:

        if packet['serverTime'] > last_processed_time:
            data = {
                "serverTime": packet['serverTime'],
                "satelliteName": packet['satellite'],
                "batteryVolts": packet['parsed']['payload']['batteryVolts'],
                "batteryCurrent": packet['parsed']['payload']['batteryCurrent'],
                "power": packet['parsed']['payload']['tinygsTxPower'],
                "temperature": packet['parsed']['payload']['tinygsTemp'],
                "position": f"{packet['satPos']['lat']},{packet['satPos']['lng']}",
                "altitude": packet['satPos']['alt']
            }
            es.index(index=index_name, document=data)
            new_packets += 1

    print(f'{new_packets} new packets received')

    last_processed_time = api[0]['serverTime']
    print(f'Last packet time: {last_processed_time}')

    sleep(180)
