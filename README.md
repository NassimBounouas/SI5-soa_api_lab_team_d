# SI5-soa_api_lab_team_d_ordering_service

### Author
__Rudy MEERSMAN__
### Updated
__30/09/2018__

## Remarks

## Requirements
```
pip install flask
pip3 install PyMySQL
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
    "Action" : "order_meal",
    "Message" :
    {
        "Meal" : "Ramen"
    }
}
```

>response
```json
{ 
     "Action": "compute_eta",  
     "Message": 
     {
	"Meal": "Ramen",
        "Price": 5,
        "Restaurant": "Lyianhg Restaurant"
     }
}
```

### Validation

* Return json of Order with unique ID for command or the command done

> Request Body 
>> validation
```json
{
    "Action" : "validate_order",
    "Message" :
    {
        "Meal": "Ramen",
        "Restaurant": "Lyianhg Restaurant",
        "Delivery_Address": "Templier",
        "Delivery_Date": "date",
        "Price": 5
    }
}
```
>> request
```json
{
    "Action" : "validation_request",
    "Message" :
    {
        "Id" : 1
    }
}
```

Example :


```json
{
    "Action" : "validate_order",
    "Message" :
    {
        "Meal" : "Ramen",
        "Restaurant" : "Lyianhg Restaurant",
        "Delivery_Address" : "Les Templiers",
        "Delivery_Date" : "Sun, 07 Oct 2018 14:41:31 GMT",
        "Price" : 5
    }
}
```

>response
```json
{  
    "Message": 
    {
        "Command_Id": 4,
        "Delivery_Address": "Les Templiers",
        "Delivery_Date": "Sun, 07 Oct 2018 14:41:31 GMT",
        "Meal": "Ramen",
        "Restaurant": "Lyianhg Restaurant"
    },
    "Status": "Accepted"
}
```

  
