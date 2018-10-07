#!/bin/bash
curl -X POST -i http://localhost:8080/receive_event --data '{
"Action":"Receive_order",
"Message": "{\"Meal\":\"Ramen\",\"RestaurantAdress\":\"Lyangsrestaurant\",\"DeliveryAdress\":\"Polytech Nice Sophia\"}"
}'
