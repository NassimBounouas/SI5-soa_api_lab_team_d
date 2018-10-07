# SI5-soa_api_lab_team_d_delivery_service


### Author
__Nassim BOUNOUAS__
### Updated
__15:26 30/09/2018__

## Remarks

The database is mocked before each request.

Only `Read` operations are available.

## Requirements

```bash
go get github.com/gorilla/mux
go get github.com/go-sql-driver/mysql

docker pull uberoolab/team-d-delivery-database
docker run -d -p 4001:3306 -t uberoolab/team-d-delivery-database

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
`docker pull uberoolab/team-d-chinese-delivery-service`

### Run (Interactive)
`docker run -i -p 4000:8080 -t uberoolab/team-d-delivery-service`

### Run (Detached)
`docker run -d -p 4000:8080 -t uberoolab/team-d-delivery-service`

## API Usage

### Request a delivery

__Example :__

> [POST] http://localhost:4000/receive_event

Payload :
```json
{
    "Action":"Delivery_request",
    "Message": "{\"Meal\":\"ORDERED_MEAL\",\"PickupAddress\":\"RESTAURANT_ADRESS\",\"PickUpDate\":\"PICKUP_DATE\",\"Client\":\"CLIENT_NAME\",\"DeliveryAdress\":\"DELIVERY_ADRESS\"}"
}
```
The PICKUP_DATE must respected the RFC3339 format : ```2018-10-10T12:00:00+02:00```

Response :
```json
{
    "Action":"Response",
    "Message":"Your request has been accepted, your ORDERED_MEAL will be picked up from RESTAURANT_ADRESS at PICKUP_DATE and delivered to DELIVERY_ADRESS"
}
```

__Example :__

Payload :
```json
{
    "Action":"Delivery_request",
    "Message": "{\"Meal\":\"Ramen\",\"PickupAddress\":\"Lyangs restaurant\",\"PickUpDate\":\"2018-10-10T12:00:00+02:00\",\"Client\":\"Philippe C.\",\"DeliveryAdress\":\"Polytech Nice Sophia\"}"
}
```

Response :
```json
{   "Action":"Response",
    "Message":"Your request has been accepted, your Ramen will be picked up from Lyangs restaurant at 2018-10-10T12:00:00+02:00 and delivered to Polytech Nice Sophia"}
```