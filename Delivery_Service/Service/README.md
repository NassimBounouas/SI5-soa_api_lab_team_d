# SI5_soa_api_lab_team_d_menu_service

### Author
__Nikita ROUSSEAU__
### Updated
__17:00 01/11/2018__

## Remarks

The database is populated (if needed) before each request

Only `Read` operations are available.

## Requirements

- Python 3.6.x
- Dependencies :
  * PyMySQL
  * kafka-python

### Install Dependencies

```bash
pip install --trusted-host pypi.python.org -r requirements.txt
```

## Server Startup

```bash
python3 app.py <production|development>
INFO:root:Starting...
INFO:root:Ready !
INFO:root:Serving application in `development` environment
```

## Database Configuration

You can configure database connection in `db.ini`

```ini
# Application Configuration File
# Loaded on-the-fly regarding the first passed argument (production|development)

[development]
# DATABASE
host=localhost
port=3306
user=root
pass=
db=soa
# KAFKA
bootstrap_servers=mint-virtual-machine:9092,

[production]
# DATABASE
host=menu-database
port=3306
user=root
pass=root
db=soa
# KAFKA
bootstrap_servers=kafka:9092,
```

## Docker

### Build
`docker build -t menuapp .`

### Run
`docker run menuapp`

### Publish
```bash
mint-virtual-machine # docker login --username=nrousseauetu
Password: 
Login Succeeded
mint-virtual-machine # docker images
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
menuapp             latest              dea9321cc24c        7 minutes ago       155MB
python              3.6.5-slim          b31cb11e68a1        3 months ago        138MB
mint-virtual-machine # docker tag dea9321cc24c uberoolab/team-d-menu-service:latest
mint-virtual-machine # docker push uberoolab/team-d-menu-service
The push refers to repository [docker.io/uberoolab/team-d-menu-service]
[...]
```

### Pull From Hub
`docker pull uberoolab/team-d-delivery-service`

### Run From Hub (Interactive)
`docker run -i -t uberoolab/team-d-delivery-service`

### Run From Hub (Detached)
`docker run -d -t uberoolab/team-d-delivery-service`

## Service Usage

### Request a delivery

Usage :

> [KAFKA] `delivery` topic
```json
{
  "action": "DELIVERY_REQUEST",
  "message": {
    "request":42,
    "meal_name": "Ramen",
    "pickup_restaurant": "Tiberdor",
    "pickup_date": "2018-11-02 12:00",
    "delivery_address": "Chez moi"
  }
}
```
Response : `Service is not generating any response` 

## Examples

Using `kafka-console-producer.sh`

```bash
$ ./bin/kafka-console-producer.sh --broker-list localhost:9092 --topic delivery
>{"action": "DELIVERY_REQUEST", "message": {"request":42, "meal_name": "Ramen", "pickup_restaurant": "Tiberdor", "pickup_date": "2018-11-02 12:00", "delivery_address": "Chez moi"}}
```
