# SI5-soa_api_lab_team_d_payment_service

### Author
__Duminy Gaétan__
### Updated
__14:30 01/11/2018__

## Remarks

The application was developed under Windows 10 with Eclipse and the PyDev module.

## Requirements

```
pip install kafka-python
```

## Server Startup

```
With Eclipse: PaywallService.py > right-click > Run As > Python Run
```

## Communicate with the kafka topic

```
-Open Zookeeper
-Open Kafka
-Create the topic "ordering"
-Create the topic "payment"
```

## API Usage

### Payment Placed

Send a Json on the kafka topic "ordering" and give a response on the same topic.

**Examples:**

Example of request:

```
{	
     "action": "PAYMENT_PLACED",
     "message": {
	"request": 1001,
	"card_number": 1234123412341234,
	"shipping_address": "10 rue du test"
     }
}
```

Example of answer:
```
{
    "action": "PAYMENT_ACCEPTED",
    "message": {
	"status": "OK",
    	"request": 1001
    }
}
```

### Notify Delivery Response

Send a Json on the kafka topic "payment" and don't give response.

```
{	
    "action": "NOTIFY_DELIVERY_RESPONSE"
    "message": {
	"request": 1001
    }
}
```

> Note :

> The actions of this service are simulate
