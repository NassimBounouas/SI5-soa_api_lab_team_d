# SI5-soa_api_lab_team_d_ordering_service

### Author
__Rudy MEERSMAN__
### Updated
__30/09/2018__

## Remarks
The Database is a json file named "Restaurant.json" where there's meals with theirs Restaurant
```json
{
  "Plat" : [
    {
      "Id": 1,
      "Name": "Ramen",
      "Restaurant": "Lyianhg Restaurant"
    },
    {
      "Id": 2,
      "Name": "Pizza",
      "Restaurant": "Bar Roger"
    }
  ]
}
```

## Requirements
```
pip install flask
```

## API Usage

* Request type :: [POST] http://127.0.0.1:4001/receive_event

### Restaurant

* Get Restaurant who make the meal ::

> Request Body 

```json
{
    "Action" : "order_meal",
    "Message" :
    {
        "Meal": "Ramen"
    }
}
```


Example :

>with "Meal" : "Ramen"
> [POST] http://127.0.0.1:4001/receive_event

```json
{
    "Action": "compute_eta",
    "Message": {
        "Meal": "Ramen",
        "Restaurant": "Lyianhg Restaurant"
    }
}
```

### Validation

* Return json of Order with unique ID for command

> Request Body 

```json
{
    "Action" : "validate_order",
    "Message" :
    {
        "Meal": "Ramen",
        "Restaurant": "Lyianhg Restaurant",
        "Delivery_Address": "Templier",
        "Pick_Up_Date": "40",
        "Delivery_Date": "60"
    }
}
```

Example :


```json
{
    "Action": {
        "Command_Id": 47,
        "Delivery_Address": "Templier",
        "Delivery_Date": "60",
        "Meal": "Ramen",
        "Restaurant": "Lyianhg Restaurant"
    },
    "Status": "Accepted"
}
```


  
