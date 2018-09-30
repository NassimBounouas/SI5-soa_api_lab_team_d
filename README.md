# SI5_soa_api_lab_team_d_chinese_restaurant_service

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
"Message": "{\"Meal\":\"YOUR_MEAL\",\"RestaurantAdress\":\"THE_RESTAURANT\",\"DeliveryAdress\":\"DELIVERY_LOCATION\"}"
}
```

Response :
```json
{
    "response": "Order received, YOUR_MEAL in preparation"
}
```

__Example :__

Payload :
```json
{
"Action":"Receive_order",
"Message": "{\"Meal\":\"Ramen\",\"RestaurantAdress\":\"Liang restaurant\",\"DeliveryAdress\":\"Polytech Nice Sophia\"}"
}
```

Response :
```json
{
    "response": "Order received, Ramen in preparation"
}
```