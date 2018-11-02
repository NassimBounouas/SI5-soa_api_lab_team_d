# Restaurant_Service

### Author
__Nikita ROUSSEAU__
### Updated
__01:00 02/11/2018__

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

// TODO

## Service Usage

### List categories

Usage :

> [KAFKA] `restaurant` topic
```json
{
  "action": "RESTAURANT_LIST_REQUEST",
  "message": {
    "request": 42
  }
}
```

Response :

```json
{
  "action": "RESTAURANT_LIST_RESPONSE",
  "message": {
    "status": "OK",
    "request": 42,
    "restaurants": [
      {
        "id": 11,
        "name": "Dragon d'Or"
      },
      {
        "id": 12,
        "name": "Le cercle des Yakuzas"
      }
    ]
  }
}
```

## Examples

Using `kafka-console-producer.sh`

```bash
$ ./bin/kafka-console-producer.sh --broker-list localhost:9092 --topic restaurant
>{"action":"RESTAURANT_LIST_REQUEST","message":{"request":42}}
```
