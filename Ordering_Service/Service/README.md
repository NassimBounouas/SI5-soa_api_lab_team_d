# SI5-soa_api_lab_team_d_ordering_service

### Author
__Rudy MEERSMAN__
### Updated
__07/10/2018__

## Remarks

## Requirements
```
pip install kafka-python
pip3 install PyMySQL
```

## API Usage

* Request type :: [POST] http://127.0.0.1:4001/receive_event

### Validation

* Return json of Order with unique ID for command or the command done

> Request Body 
>> validation
```json
{	"Action" : "ORDER_REQUEST"
	,"Message" :
	{
		"id meal" : 46,
		"id restaurant" : "Lyianhg Restaurant",
		"client name" : "Victor",
		"client address" : "les Templier"
	}
}
```
Example :


```json
{	"Action" : "VALIDATE_ORDER",
	"Message" :
	{	
		"Id": 85
	}
}
```

>response
```json
{	"Action": "PREPARE_COMMAND", 
	"Message": 
	{
		"id_request": 85,
		"id_restaurant": "Lyianhg Restaurant",
		"id_meal": "46"
	}
}
```

  
