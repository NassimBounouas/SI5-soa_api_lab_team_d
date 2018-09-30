# SI5-soa_api_lab_team_d_eta_computer_service

### Author
__Duminy Gaétan__
### Updated
__16:00 30/09/2018__

## Remarks

The application was developed under Windows 10 with Eclipse and the PyDev module.

## Requirements

```
pip install flask
```

## Server Startup

```
With Eclipse: Eta.py > right-click > Run As > Python Run
```

## Communicate with the server

```
With Postman: 
  -Post a Json: -Select POST then enter the following URL, http://127.0.0.1:4002/receive_event
                -Go on Body, select raw and then choose JSON (application/json) from the drop-down menu
                -Write your Json and click on Send
		-The server return a Json
```

## API Usage

### Compute Eta

Post a Json with [POST] http://127.0.0.1:4002/receive_event and the server will return a Json including Eta.

The **delivery date** is the time estimated by the system for the customer to receive his order.

The **pick up date** is the time estimated by the system for the delivery person to pick up the order from the restaurant.

**Examples:**

Example of request:

```
{
	"Meal": "Sushi",
	"Restaurant": "Le soleil de l'est",
	"DeliveryAddress": "Campus Templier"
}
```

Example of answer:
```
{
    "DeliveryAddress": "Campus Templier",
    "DeliveryDate": 29,
    "Meal": "Sushi",
    "PickUpDate": 17,
    "Restaurant": "Le soleil de l'est"
}
```

> Note :
> The times indicated by ETA are currently simple random integers
