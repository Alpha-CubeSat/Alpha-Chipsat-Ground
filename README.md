# ChipSat Ground Station

Ground station software to receive and process telemetry from ChipSats part of the Alpha CubeSat mission.

## Overview
Connects to the API of the [tinygs](https://tinygs.com/) ground station network (a global network of LoRa ground stations)
After a set time interval, it fetches the API and checks for new packets. New packets are then sent to an elasticsearch database. The data is then displayed in a kibana dashboard with different data views.

## Dependencies
- Python version >= 3.9
- Python dependencies (run pip install -r requirements.txt)
- Elasticsearch 8.4.3
- Kibana 8.4.3

## Running the Ground Station
This section provides instructions on setting up the environment and running the ground station.

1. **Install Elasticsearch**.  ElasticSearch is what the ground system uses to store telemetry data that is retrieved from TinyGS. The correct Elasticsearch version can be found [here](https://www.elastic.co/guide/en/elasticsearch/reference/8.4/install-elasticsearch.html). By default ElasticSearch should listen on `localhost:9200`. This can be changed in the configuration file at `/etc/elasticsearch/elasticsearch.yml`. For local installations, Elasticsearch can be started with `.\bin\elasticsearch.bat`. Comprehensive documentation can be found [here](https://www.elastic.co/guide/en/elasticsearch/reference/8.4/elasticsearch-intro.html). 

After running `.\bin\elasticsearch.bat`, user credentials should appear in the command line window. The enrolllment token is needed for the Kibana installation. Copy the elastic user password and create a new file called creds.py that contains a tuple called elastic_auth in the format of ('elastic','PASSWORD') where the elastic user password replaces PASSWORD.

In `/etc/elasticsearch/config/certs` drag the file http_ca.crt into the cloned Alpha-Chipsat-Ground directory. 

2. **Install Kibana**. Kibana is used as a data visualization tool to display the received telemetry data in several data views. The correct Kibana version can be found [here](https://www.elastic.co/guide/en/kibana/8.4/install.html). Kibana can be configured through the configuration file at `/etc/kibana/kibana.yml` By default Kibana listens on `localhost:5601`. For local installations, Elasticsearch can be started with `.\bin\kibana.bat`. Comprehensive documentation can be found [here](https://www.elastic.co/guide/en/kibana/8.4/introduction.html)

To use the existing data layout, import the dashboard.ndjson as a Kibana dashboard. The existing layout contains battery current, battery voltage, power, temperature, position, and altitude data.

3. **Run ground_station.py** ground_station.py accesses the [tinygs](https://tinygs.com/) API, receives and processes new packets, and sends the data into an elasticsearch database. ground_station.py should run continuously in the background while the ground station is running. 