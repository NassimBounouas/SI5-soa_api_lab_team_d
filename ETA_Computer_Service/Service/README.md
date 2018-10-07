# SI5-soa_api_lab_team_d_eta_computer_service

### Author
__Duminy Gaétan__
### Updated
__16:20 01/10/2018__

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

The **delivery date** is the date estimated by the system for the customer to receive his order.

The **pick up date** is the date estimated by the system for the delivery person to pick up the order from the restaurant.

**Examples:**

Example of request:

```
{	
	"Action": "compute_eta",
    	"Message": {
	"Meal": "Sushi",
	"Restaurant": "Le soleil de l'est",
	"Delivery_Address": "Campus Templier"
	}
}
```

Example of answer:
```
{
    "Action": "validate_order",
    "Message": {
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