# SI5_soa_api_lab_team_d_menu_service

### Author
__Nikita ROUSSEAU__
### Updated
__16:00 30/09/2018__

## Remarks

The database is mocked before each request.

Only `Read` operations are available.

## Requirements

```bash
pip install flask
```

## Server Startup

```bash
export FLASK_APP=app.py
export FLASK_ENV=development

flask run --host 0.0.0.0 --port 5000

# * Serving Flask application
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
	"Action": "READ_CATEGORIES",
	"Message": {}
}
```

Response :

```json
{
    "categories": [
        {
            "id": 1,
            "name": "Japonais",
            "region": "Asie"
        },
        {
            "id": 2,
            "name": "Chinois",
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
            "category": "Japonais",
            "id": 1,
            "is_menu": false,
            "name": "Sushis saumon",
            "price": 3.9
        },
        {
            "category": "Japonais",
            "id": 2,
            "is_menu": false,
            "name": "Sushis saumon épicé",
            "price": 4.5
        },
        {
            "category": "Japonais",
            "id": 3,
            "is_menu": false,
            "name": "Sushis saumon mariné au jus de yuzu et ses herbes",
            "price": 4.8
        },
        {
            "category": "Japonais",
            "id": 5,
            "is_menu": true,
            "name": "Plateau 1 - 8 pièces",
            "price": 13.9
        }
    ],
    "status": "OK"
}
```

> Note :
> The category must be passed by the category name
