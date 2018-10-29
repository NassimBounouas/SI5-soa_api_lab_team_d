# SI5-soa_api_lab_team_d_ordering_service

### Author
__Rudy MEERSMAN__
### Updated
__29/10/2018__

## Remarks

## Requirements
```
pip3 install kafka-python
pip3 install PyMySQL
```

## API Usage

* Request type :: [POST] http://127.0.0.1:4001/receive_event

### Validation

* Save in database the order and create an ID for this command

> Request Body 
>> validation
```json
{	"action" : "order_request",
	"message" :
	{
		"id meal" : 46,
		"id restaurant" : "Lyianhg Restaurant",
		"client name" : "Victor",
		"client address" : "les Templier"
	}
}
```

* Get the order with his id from database and return a "PREPARE_COMMAND" action:
```json
{	"action" : "validate_order",
	"message" :
	{	
		"Id": 85
	}
}
```

>response
```json
{	"action": "prepare_command", 
	"message": 
	{
		"id_request": 85,
		"id_restaurant": "Lyianhg Restaurant",
		"id_meal": "46"
	}
}
```

  
