#!/bin/bash

echo -e " \n\n### REQUEST MENU TO MENU SERVICE\n"
curl -s -X POST --header "Content-Type: application/json" http://localhost:4000/receive_event --data '{
	"Action": "READ_CATEGORIES",
	"Message": {}
}' | json_pp

echo -e " \n\n### REQUEST MENU WITH JAPANASE CATEGORY\n"
curl -s -X POST --header "Content-Type: application/json" http://localhost:4000/receive_event --data '{
	"Action": "READ_MEALS_BY_CATEGORY",
	"Message": {
		"Category": "Japonais"
	}
}' | json_pp

echo -e " \n\n### ORDER A RAMEN MEAL\n"
curl -s -X POST http://localhost:4001/receive_event --data '{
    "action" : "order_meal",
    "message" :
    {
        "meal": "Ramen"
    }
}' | json_pp

echo -e " \n\n### VALIDATE THE RAMEN MEAL ORDER\n"
curl -s -X POST http://localhost:4001/receive_event --data '{
    "action" : "validate_order",
    "message" :
    {
        "meal": "Ramen",
        "restaurant": "Lyianhg Restaurant",
        "delivery_address": "Templier",
        "pick_up_date": "40",
        "delivery_date": "60",
        "price" : "15.00€"
    }
}' | json_pp

echo -e " \n\n### SENDING ORDER TO RESTAURANT SERVICE\n"
curl -X POST http://localhost:4003/receive_event --data '{
"Action":"Receive_order",
"Message": "{\"Meal\":\"Ramen\",\"RestaurantAdress\":\"Lyangsrestaurant\",\"DeliveryAdress\":\"Polytech Nice Sophia\"}"
}'

echo -e "\n\n### SENDING DELIVERY REQUEST TO DELIVERY SERVICE\n"
curl -X POST http://localhost:4004/receive_event --data '{
"Action":"Delivery_request",
"Message": "{\"Meal\":\"Ramen\",\"RestaurantAdress\":\"Lyangsrestaurant\",\"DeliveryAdress\":\"Polytech Nice Sophia\"}"
}'

echo -e "\n\n"
