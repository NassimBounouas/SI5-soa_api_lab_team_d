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
	"Action": "ETA_REQUESTED",
    	"Message": {
	"ID_Request": 1001,
	"Meal": "Sushi",
	"Restaurant": "Le soleil de l'est",
	"Delivery_Address": "Campus Templier"
	}
}
```

Example of answer:
```
{
    "Action": "ETA_RESPONSE",
    "Message": {
    	"ID_Request": 1001,
        "Delivery_Address": "Campus Templier",
        "Delivery_Date": "Sun, 07 Oct 2018 14:54:31 GMT",
        "Meal": "Sushi",
        "Pick_Up_Date": "Sun, 07 Oct 2018 14:41:31 GMT",
        "Restaurant": "Le soleil de l'est"
    }
}
```

> Note :
> The times indicated by ETA are currently simple random integers
> Data type is now a String
