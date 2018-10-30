# UberooApiGateway

### Author
__Nikita ROUSSEAU__
### Updated
__00:00 30/10/2018__

## Requirements

- Python 3.6.x
- Dependencies :
  * flask
  * kafka-python

### Install Dependencies

```bash
pip install --trusted-host pypi.python.org -r requirements.txt
```

## Deployment

You can start the server in (`development`|`production`) environment. Set `FLASK_ENV` according to your needs.

```bash
export FLASK_APP = app.py
export FLASK_ENV = development
export FLASK_DEBUG = 1

$ python3 app.py

WARNING:root:Uberoo Api Gateay version 1.0 (development) is starting...
WARNING:root:It may take up to 60 seconds before running !
INFO:kafka.client:Bootstrapping cluster metadata from [('mint-virtual-machine', 9092, <AddressFamily.AF_UNSPEC: 0>)]
 * Serving Flask app "app" (lazy loading)
 * Environment: development
 * Debug mode: on
INFO:kafka.conn:<BrokerConnection node_id=bootstrap host=mint-virtual-machine:9092 <connecting> [IPv4 ('192.168.49.128', 9092)]>: connecting to mint-virtual-machine:9092 [('192.168.49.128', 9092) IPv4]
INFO:kafka.conn:<BrokerConnection node_id=bootstrap host=mint-virtual-machine:9092 <connecting> [IPv4 ('192.168.49.128', 9092)]>: Connection complete.
INFO:kafka.client:Bootstrap succeeded: found 1 brokers and 2 topics.
INFO:kafka.conn:<BrokerConnection node_id=bootstrap host=mint-virtual-machine:9092 <connected> [IPv4 ('192.168.49.128', 9092)]>: Closing connection. 
INFO:kafka.conn:<BrokerConnection node_id=0 host=mint-virtual-machine:9092 <connecting> [IPv4 ('192.168.49.128', 9092)]>: connecting to mint-virtual-machine:9092 [('192.168.49.128', 9092) IPv4]
INFO:kafka.conn:Probing node 0 broker version
INFO:kafka.conn:<BrokerConnection node_id=0 host=mint-virtual-machine:9092 <connecting> [IPv4 ('192.168.49.128', 9092)]>: Connection complete.
INFO:kafka.conn:Broker version identifed as 1.0.0
INFO:kafka.conn:Set configuration api_version=(1, 0, 0) to skip auto check_version requests on startup
INFO:werkzeug: * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
```

## Docker

### Build
`docker build -t uberooapigateway .`

### Run
`docker run -p 5000:5000 uberooapigateway`

### Publish
```bash
mint-virtual-machine # docker login --username=nrousseauetu
Password: 
Login Succeeded
mint-virtual-machine # docker images
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
uberooapigateway    latest              dea9321cc24c        7 minutes ago       155MB
python              3.6.5-slim          b31cb11e68a1        3 months ago        138MB
mint-virtual-machine SI5_soa_api_lab_team_d_menu_service # docker tag dea9321cc24c uberoolab/team-d-apigateway:latest
mint-virtual-machine SI5_soa_api_lab_team_d_menu_service # docker push uberoolab/team-d-apigateway
The push refers to repository [docker.io/uberoolab/team-d-apigateway]
[...]
```

### Pull From Hub
`docker pull uberoolab/team-d-apigateway`

### Run From Hub (Interactive)
`docker run -i -p 5000:5000 -t uberoolab/team-d-apigateway`

### Run From Hub (Detached)
`docker run -d -p 5000:5000 -t uberoolab/team-d-apigateway`

## Api Documentation

// TODO

## Notes
http://y.tsutsumi.io/global-logging-with-flask.html

http://flask.pocoo.org/docs/1.0/appcontext/
https://github.com/miguelgrinberg/Flask-SocketIO/issues/372
https://scotch.io/tutorials/build-a-distributed-streaming-system-with-apache-kafka-and-python