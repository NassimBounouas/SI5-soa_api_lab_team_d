# SI5-soa_api_lab_team_d_ordering_service

### Author
__Rudy MEERSMAN__
### Updated
__30/09/2018__

## Remarks
The Database is a json file named "Restaurant.json" where there's meals with theirs Restaurant
```json
{
  "plat" : [
    {
      "id": 1,
      "name": "Ramen",
      "restaurant": "Lyianhg Restaurant",
      "price" : "3.50"
    },
    {
      "id": 2,
      "name": "Pizza",
      "restaurant": "Bar Roger",
      "price" : "6.00"
    }
  ]
}
```

## Requirements
```
pip install flask
```

## API Usage

* Request type :: [GET] http://127.0.0.1:4001/receive_event

### Restaurant

* Get Restaurant who make the meal ::

> Request Body 

```json
{
    "action" : "order_meal",
    "message" :
    {
        "meal": something
    }
}
```


Example :

>with "meal" : "Ramen"
> [GET] http://127.0.0.1:4001/receive_event

```json
{
    "action": "compute_eta",
    "message": {
        "meal": "Ramen",
        "price": "3.50",
        "restaurant": "Lyianhg Restaurant"
    }
}
```

### Validation

* Return json of Order with unique ID for command

> Request Body 

```json
{
    "action" : "validate_order",
    "message" :
    {
        "meal": "Ramen",
        "restaurant": "Lyianhg Restaurant",
        "delivery_address": "Templier",
        "pick_up_date": "40",
        "delivery_date": "60",
        "price" : "15.00€"
    }
}
```

Example :


```json
{
    "action": {
        "command_id": 47,
        "delivery_address": "Templier",
        "delivery_date": "60",
        "meal": "Ramen",
        "price": "15.00€",
        "restaurant": "Lyianhg Restaurant"
    },
    "status": "Accepted"
}
```


  
