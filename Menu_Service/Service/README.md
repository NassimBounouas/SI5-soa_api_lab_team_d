# SI5_soa_api_lab_team_d_menu_service

### Author
__Nikita ROUSSEAU__
### Updated
__19:00 27/10/2018__

## Remarks

The database is populated (if needed) before each request

Only `Read` operations are available.

## Requirements

- Python 3.6.x
- Dependencies :
```bash
pip install PyMySQL
pip install kafka-python
pip install jsonify
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
bootstrap_servers=0.0.0.0:9092,
```

## Docker

### Build
`docker build -t menuapp .`

### Run
`docker run -p 5000:5000 menuapp`

### Publish
```bash
mint-virtual-machine SI5_soa_api_lab_team_d_menu_service # docker login --username=nrousseauetu
Password: 
Login Succeeded
mint-virtual-machine SI5_soa_api_lab_team_d_menu_service # docker images
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
menuapp             latest              dea9321cc24c        7 minutes ago       155MB
python              3.6.5-slim          b31cb11e68a1        3 months ago        138MB
mint-virtual-machine SI5_soa_api_lab_team_d_menu_service # docker tag dea9321cc24c uberoolab/team-d-menu-service:latest
mint-virtual-machine SI5_soa_api_lab_team_d_menu_service # docker push uberoolab/team-d-menu-service
The push refers to repository [docker.io/uberoolab/team-d-menu-service]
[...]
```

### Pull From Hub
`docker pull uberoolab/team-d-menu-service`

### Run From Hub (Interactive)
`docker run -i -p 5000:5000 -t uberoolab/team-d-menu-service`

### Run From Hub (Detached)
`docker run -d -p 5000:5000 -t uberoolab/team-d-menu-service`

## API Usage

### Endpoint as Event listener

> [POST] http://127.0.0.1:5000/receive_event

### List categories

Usage :

> [KAFKA] `restaurant` topic
```json
{
  "Action": "CATEGORY_LIST_REQUEST",
  "Message": {}
}
```

Response :

```json
{
  "Action": "CATEGORY_LIST_RESPONSE",
  "Status": "OK",
  "Categories": [
    {
      "id": 11,
      "name": "Japonais",
      "region": "Asie"
    },
    {
      "id": 12,
      "name": "Chinois",
      "region": "Asie"
    }
  ]
}
```

### List meals by category name

Usage :

> [KAFKA] `restaurant` topic
```json

```

Response :

```json

```

> Note :
> The category must be passed by the category name

## Example with cURL

Read categories with `kafka-console-producer.sh`

```bash
$ ./bin/kafka-console-producer.sh --broker-list localhost:9092 --topic restaurant
>{"Action":"CATEGORY_LIST_REQUEST","Message":{}}
```
