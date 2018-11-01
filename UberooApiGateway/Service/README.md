# UberooApiGateway

### Author
__Nikita ROUSSEAU__
### Updated
__17:00 01/11/2018__

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
INFO:kafka.client:Bootstrapping cluster metadata from [('mint-virtual-machine', 9092, <AddressFamily.AF_UNSPEC: 0>)]
INFO:kafka.client:Bootstrapping cluster metadata from [('mint-virtual-machine', 9092, <AddressFamily.AF_UNSPEC: 0>)]
INFO:kafka.client:Bootstrapping cluster metadata from [('mint-virtual-machine', 9092, <AddressFamily.AF_UNSPEC: 0>)]
INFO:kafka.client:Bootstrapping cluster metadata from [('mint-virtual-machine', 9092, <AddressFamily.AF_UNSPEC: 0>)]
INFO:kafka.client:Bootstrapping cluster metadata from [('mint-virtual-machine', 9092, <AddressFamily.AF_UNSPEC: 0>)]
 * Serving Flask app "app" (lazy loading)
 * Environment: development
 * Debug mode: on
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
mint-virtual-machine # docker tag dea9321cc24c uberoolab/team-d-apigateway:latest
mint-virtual-machine # docker push uberoolab/team-d-apigateway
The push refers to repository [docker.io/uberoolab/team-d-apigateway]
[...]
```

### Pull From Hub
`docker pull uberoolab/team-d-apigateway`

### Run From Hub (Interactive)
`docker run -i -p 5000:5000 -t uberoolab/team-d-apigateway`

### Run From Hub (Detached)
`docker run -d -p 5000:5000 -t uberoolab/team-d-apigateway`

## Api Documentation and Usage

The API is self documented using a generated HTML document.

This documentation is available at the root directory of the listening server.

The swagger `YML` document *should* be packed with this project.

By default:
```
http://127.0.0.1:5000/
```
