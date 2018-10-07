#!/bin/bash

RED='\033[0;31m'
GREEN='\033[0;32m'
ORANGE='\033[0;33m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e " \n\n${RED}### REQUEST MENU TO MENU SERVICE${NC}\n"
curl -s -X POST --header "Content-Type: application/json" -i http://localhost:4000/receive_event --data '{
	"Action": "READ_CATEGORIES",
	"Message": {}
}'

echo -e " \n\n${RED}### REQUEST MENU WITH JAPANASE CATEGORY${NC}\n"
curl -s -X POST --header "Content-Type: application/json" -i http://localhost:4000/receive_event --data '{
	"Action": "READ_MEALS_BY_CATEGORY",
	"Message": {
		"Category": "Japonais"
	}
}'

echo -e " \n\n${GREEN}### ORDER A RAMEN MEAL${NC}\n"
curl -s -X POST -i http://localhost:4001/receive_event --data '{
    "Action" : "order_meal",
    "Message" :
    {
        "Meal": "Ramen"
    }
}'

echo -e " \n\n${ORANGE}### COMPUTE ETA FOR THE ORDER${NC}\n"
curl -X POST -H 'Content-Type: application/json' -i http://localhost:4002/receive_event --data '{	
	"Action": "compute_eta",
    	"Message": {
	"Meal": "Ramen",
	"Restaurant": "Lyianhg Restaurant",
	"Delivery_Address": "Polytech Nice Sophia"
	}
}'

echo -e " \n\n${GREEN}### VALIDATE THE RAMEN MEAL ORDER${NC}\n"
curl -s -X POST -i http://localhost:4001/receive_event --data '{
    "Action" : "validate_order",
    "Message" :
    {
        "Meal": "Ramen",
        "Restaurant": "Lyianhg Restaurant",
        "Delivery_Address": "Polytech Nice Sophia",
        "Pick_Up_Date": "40",
        "Delivery_Date": "60",
        "Price" : "15.00€"
    }
}'

echo -e " \n\n${BLUE}### SENDING ORDER TO RESTAURANT SERVICE${NC}\n"
curl -s -X POST -i http://localhost:4003/receive_event --data '{
"Action":"Receive_order",
"Message": "{\"Meal\":\"Ramen\",\"Client\":\"Philippe C.\",\"PickUpDate\":\"2018-10-10T12:00:00+02:00\"}"
}'

echo -e "\n\n${YELLOW}### SENDING DELIVERY REQUEST TO DELIVERY SERVICE${NC}\n"
curl -s -X POST -i http://localhost:4004/receive_event --data '{
"Action":"Delivery_request",
"Message": "{\"Meal\":\"Ramen\",\"PickupAddress\":\"Lyangs restaurant\",\"PickUpDate\":\"2018-10-10T12:00:00+02:00\",\"Client\":\"Philippe C.\",\"DeliveryAdress\":\"Polytech Nice Sophia\"}"
}'

echo -e "\n\n"
