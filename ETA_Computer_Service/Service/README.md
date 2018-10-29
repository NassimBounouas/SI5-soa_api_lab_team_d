# SI5-soa_api_lab_team_d_eta_computer_service

### Author
__Duminy Gaétan__
### Updated
__15:27 29/10/2018__

## Remarks

The application was developed under Windows 10 with Eclipse and the PyDev module.

## Requirements

```
pip install kafka-python
```

## Server Startup

```
With Eclipse: Eta.py > right-click > Run As > Python Run
```

## Communicate with the kafka topic

```
-Open Zookeeper
-Open Kafka
-Create the topic "eta"
```

## API Usage

### Compute Eta

Send a Json on the kafka topic "eta" and give a response on the same topic.

The **delivery date** is the date estimated by the system for the customer to receive his order.

The **pick up date** is the date estimated by the system for the delivery person to pick up the order from the restaurant.

**Examples:**

Example of request:

```
{	
	"action": "eta_requested",
    	"message": {
	"id_request": 1001,
	"meal": "Sushi",
	"restaurant": "Le soleil de l'est",
	"delivery_address": "Campus Templier"
	}
}
```

Example of answer:
```
{
    "action": "eta_response",
    "message": {
    	"id_request": 1001,
        "delivery_address": "Campus Templier",
        "delivery_date": "Sun, 07 Oct 2018 14:54:31 GMT",
        "meal": "Sushi",
        "pick_up_date": "Sun, 07 Oct 2018 14:41:31 GMT",
        "restaurant": "Le soleil de l'est"
    }
}
```

> Note :
> The times indicated by ETA are currently simple random integers
> Data type is now a String
