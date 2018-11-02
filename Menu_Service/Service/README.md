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
`docker pull uberoolab/team-d-menu-service`

### Run From Hub (Interactive)
`docker run -i -t uberoolab/team-d-menu-service`

### Run From Hub (Detached)
`docker run -d -t uberoolab/team-d-menu-service`

## Service Usage

### List categories

Usage :

> [KAFKA] `restaurant` topic
```json
{
  "action": "CATEGORY_LIST_REQUEST",
  "message": {
    "request": 42
  }
}
```

Response :

```json
{
  "action": "CATEGORY_LIST_RESPONSE",
  "message": {
    "status": "OK",
    "request": 42,
    "categories": [
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
}
```

### List meals by category <name|id>

Usage :

> [KAFKA] `restaurant` topic

Filter by `category`:

```json
{
  "action": "FOOD_LIST_REQUEST",
  "message": {
    "request": 42,
    "category": "Japonais"
  }
}
```

Response :

```json
{
  "action": "FOOD_LIST_RESPONSE",
  "message": {
    "status": "OK",
    "request": 42,
    "meals": [
      {
        "id": 33,
        "category": {
          "id": 11,
          "name": "Japonais",
          "region": ""
        },
        "restaurant": {
          "id": 11,
          "name": "Dragon d'Or"
        },
        "name": "Sushis saumon",
        "price": 3.9,
        "is_menu": false,
        "image": ""
      }
    ]
  }
}
```

Filter by `restaurant`:

```json
{
  "action": "FOOD_LIST_REQUEST",
  "message": {
    "request": 42,
    "restaurant": 12
  }
}
```

Response :

```json
{
  "action": "FOOD_LIST_RESPONSE",
  "message": {
    "status": "OK",
    "request": 42,
    "meals": [
      {
        "id": 37,
        "category": {
          "id": 12,
          "name": "Chinois",
          "region": ""
        },
        "restaurant": {
          "id": 12,
          "name": "Le cercle des Yakuzas"
        },
        "name": "Brochette de viande au fromage",
        "price": 13.9,
        "is_menu": false,
        "image": ""
      },
      {
        "id": 38,
        "category": {
          "id": 11,
          "name": "Japonais",
          "region": ""
        },
        "restaurant": {
          "id": 12,
          "name": "Le cercle des Yakuzas"
        },
        "name": "Plateau 1 - 8 pièces",
        "price": 13.9,
        "is_menu": true,
        "image": ""
      }
    ]
  }
}
```

## Examples

Using `kafka-console-producer.sh`

```bash
$ ./bin/kafka-console-producer.sh --broker-list localhost:9092 --topic restaurant
>{"action":"CATEGORY_LIST_REQUEST","message":{"request":42}}
>{"action":"FOOD_LIST_REQUEST","message":{"request":42,"category":"Japonais"}}
>{"action":"FOOD_LIST_REQUEST","message":{"request":42,"category":12}}
>{"action":"FOOD_LIST_REQUEST","message":{"request":42,"restaurant":12}}
```