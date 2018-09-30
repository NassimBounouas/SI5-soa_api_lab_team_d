#!/bin/bash

echo -e " \n\n### SENDING ORDER TO RESTAURANT SERVICE\n"
curl -X POST -i http://localhost:4003/receive_event --data '{
"Action":"Receive_order",
"Message": "{\"Meal\":\"Ramen\",\"RestaurantAdress\":\"Lyangsrestaurant\",\"DeliveryAdress\":\"Polytech Nice Sophia\"}"
}'

echo -e "\n\n### SENDING DELIVERY REQUEST TO DELIVERY SERVICE\n"
curl -X POST -i http://localhost:4004/receive_event --data '{
"Action":"Delivery_request",
"Message": "{\"Meal\":\"Ramen\",\"RestaurantAdress\":\"Lyangsrestaurant\",\"DeliveryAdress\":\"Polytech Nice Sophia\"}"
}'
