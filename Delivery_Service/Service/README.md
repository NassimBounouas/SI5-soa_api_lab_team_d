# SI5_soa_api_lab_team_d_menu_service

### Author
__Nikita ROUSSEAU__
### Updated
__17:20 07/11/2018__

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

### Notification of delivery

Usage :

> [KAFKA] `delivery` topic
```json
{
    "action": "NOTIFY_DELIVERY_REQUEST",
       "message": {
            "request": 42,
            "id_order": 1
       }
}
```
Response : `Service is not generating any response`

### Update location of a delivery

Usage :

> [KAFKA] `delivery` topic
```json
{
    "action": "DELIVERY_LOCATION_PUSH",
    "message": {
        "request": 42,
        "id_order": 2,
        "id_steed": 1,
        "longitude": 42,
        "latitude": -53
    }
}
```
Response : `Service is not generating any response`

### Request a delivery

Usage :

> [KAFKA] `delivery` topic
```json
{
    "action": "DELIVERY_LOCALISATION_REQUESTED",
    "message": {
        "status": "OK",
        "request": 42,
        "id_order": 2
    }
}
```
Response :

> [KAFKA] `delivery` topic
```json
{
    "action": "DELIVERY_LOCATION_STATUS",
    "message": {
        "status": "OK",
        "request": 42,
        "latitude": 42,
        "longitude": -53,
        "timestamp" : "2018-11-07 13:00"
    }
}
```

### Request the stat of a Steed

Usage :

> [KAFKA] `delivery` topic
```json
{
    "action": "STEED_STAT_REQUEST",
    "message": {
        "request": 42,
        "id_steed": 1
    }
}
```
Response :
> [KAFKA] `delivery` topic
```json
{
    "action": "DELIVERY_STAT_RESPONSE",
    "message": {
        "status": "OK",
        "request": 42,
        "value" :{
            "average_pay": 13,
            "average_time": 15,
            "number_of_Delivery": 54
        }
    }
}
```


### Update a delivery if steed had a problem

Usage :

> [KAFKA] `delivery` topic
```json
{
    "action": "SEND_STEED_STATUS",
    "message": {
        "request": 42,
        "id_steed": 1,
        "status": "Accident"
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
