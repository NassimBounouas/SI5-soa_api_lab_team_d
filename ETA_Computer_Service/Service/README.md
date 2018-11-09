# SI5-soa_api_lab_team_d_eta_computer_service

### Author
__Duminy Gaétan__
### Updated
__21:48 09/11/2018__

## Remarks

The application was developed under Windows 10 with Eclipse and the PyDev module.

## Requirements

```
pip install kafka-python
```

## Communicate with the kafka topic

```
-Open Zookeeper
-Open Kafka
-Create the topic "eta"
-Create the topic "delivery"
```

## API Usage

### Compute Eta

Send a Json with, "ETA_REQUEST" on the action field and the armuments in the message field, to the kafka topic "eta" and give a response on the same topic.

**Examples:**

Example of request:

```
{   
    "action": "ETA_REQUEST",
    "message": {
	"request" : 1001,
	"from": "Le soleil de l'est",
	"to": "Campus Templier"
    }
}
```

Example of answer:
```
{
    "action": "ETA_RESPONSE",
    "message": {
        "status": "OK",
        "request": 1001,
        "from": "Le soleil de l'est",
        "to": "Campus Templier",
        "eta": 16
    }
}
```

### Update Eta

Send a Json with, "ETA_UPDATE_REQUESTED" on the action field and the armuments in the message field, to the kafka topic "delivery" and give a response on the same topic.

**Examples:**

Example of request:

```
{  
     "action": "ETA_UPDATE_REQUESTED",
     "message": {
	"request" : 1001,
	"id_order": 421,
	"to": "Campus Templier",
	"lastLatitude": 7,
	"lastLongitude": 43,
	"timestamp": "2018-11-01 12:30"
    }
}
```

Example of answer:
```
{
    "action": "DELIVERY_LOCATION_STATUS",
    "message": {
        "status": "OK",
        "request": 1001,
        "id_order": 421,
        "to": "Campus Templier",
        "lastLatitude": 7,
        "lastLongitude": 43,
        "timestamp": "2018-11-01 12:30",
        "eta": 6
    }
}
```

> **Note :**

> ETA_UPDATE_REQUESTED is the continuation of another workflow

> The times indicated by ETA are currently simple random integers

> *timestamp* type is String