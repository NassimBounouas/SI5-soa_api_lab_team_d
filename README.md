# SI5-soa_api_lab_team_d_eta_computer_service

### Author
__Duminy Gaétan__
### Updated
__13:01 30/09/2018__

## Remarks

The application was developed under Windows 10 with Eclipse and the PyDev module.

There is no database, only two global variables for the service to keep in memory the Json it receives.

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
  -Post a Json: -Select POST then enter the following URL, 127.0.0.1:5000/receiveOrder
                -Go on Body, select raw and then choose JSON (application/json) from the drop-down menu
                -Write your Json and click on Send
  -Get Eta: -Select GET then enter the following URL, 127.0.0.1:5000/computeEta
            -Click on SEND
```
