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

> [POST] http://127.0.0.1:5000/receive_event
```json
{
	"Action": "CATEGORY_LIST_REQUEST",
	"Message": {}
}
```

Response :

```json
{
    "categories": [
        {
            "id": 10,
            "name": "Chinois",
            "region": "Asie"
        },
        {
            "id": 9,
            "name": "Japonais",
            "region": "Asie"
        }
    ],
    "status": "OK"
}
```

### List meals by category name

Usage :

> [POST] http://127.0.0.1:5000/receive_event
```json
{
	"Action": "READ_MEALS_BY_CATEGORY",
	"Message": {
		"Category": "Japonais"
	}
}
```

Response :

```json
{
    "meals": [
        {
            "category": {
                "id": 9,
                "name": "Japonais",
                "region": ""
            },
            "id": 28,
            "image": "",
            "is_menu": false,
            "name": "Sushis saumon",
            "price": 3.9
        },
        {
            "category": {
                "id": 9,
                "name": "Japonais",
                "region": ""
            },
            "id": 27,
            "image": "",
            "is_menu": true,
            "name": "Plateau 1 - 8 pièces",
            "price": 13.9
        },
        {
            "category": {
                "id": 9,
                "name": "Japonais",
                "region": ""
            },
            "id": 29,
            "image": "",
            "is_menu": false,
            "name": "Sushis saumon épicé",
            "price": 4.5
        },
        {
            "category": {
                "id": 9,
                "name": "Japonais",
                "region": ""
            },
            "id": 30,
            "image": "",
            "is_menu": false,
            "name": "Sushis saumon mariné au jus de yuzu et ses herbes",
            "price": 4.8
        },
        {
            "category": {
                "id": 9,
                "name": "Japonais",
                "region": ""
            },
            "id": 31,
            "image": "",
            "is_menu": false,
            "name": "Ramen nature",
            "price": 7
        }
    ],
    "status": "OK"
}
```

> Note :
> The category must be passed by the category name

## Example with cURL

Read categories with cURL

```bash
curl -X POST http://localhost:5000/receive_event -H "Content-Type: application/json" --data '{
    "Action": "READ_CATEGORIES",
    "Message": {}
}'
```
