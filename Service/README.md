# SI5_soa_api_lab_team_d_chinese_restaurant_service

### Author
__Nassim BOUNOUAS__
### Updated
__02:14 07/10/2018__

## Requirements

```bash
go get github.com/gorilla/mux
go get github.com/go-sql-driver/mysql

docker pull uberoolab/team-d-chinese-restaurant-database
docker run -d -p 4001:3306 -t uberoolab/team-d-chinese-restaurant-database

export DATABASE=127.0.0.1:4001
```

## Build

```bash
go build -o main
```
## Server Startup

```bash
./main
```

## Docker

### Pull
`docker pull uberoolab/team-d-chinese-restaurant-service`

### Run (Interactive)
`docker run -i -p 4000:8080 -t uberoolab/team-d-chinese-restaurant-service`

### Run (Detached)
`docker run -d -p 4000:8080 -t uberoolab/team-d-chinese-restaurant-service`

## API Usage

### Order a meal

__Example :__

> [POST] http://localhost:4000/receive_event

Payload :
```json
{
    "Action":"Receive_order",
    "Message": "{\"Meal\":\"ORDERED_MEAL\",\"Client\":\"CLIENT_NAME\",\"PickUpDate\":\"PICKUP_DATE\"}"
}
```
The PICKUP_DATE must respected the RFC3339 format : ```2018-10-10T12:00:00+02:00```

Response :
```json
{   "Action":"Response",
    "Message":"Order received, ORDERED_MEAL in preparation to be picked up at : PICKUP_DATE"
}
```

__Example :__

Payload :
```json
{
    "Action":"Receive_order",
    "Message": "{\"Meal\":\"Ramen\",\"Client\":\"Philippe C.\",\"PickUpDate\":\"2018-10-10T12:00:00+02:00\"}"
}
```

Response :
```json
{
    "Action":"Response",
    "Message":"Order received, Ramen in preparation to be picked up at : 2018-10-10T12:00:00+02:00"
}
```