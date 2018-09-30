package main

import "time"

type Order struct {
	Meal string
	RestaurantAdress string
	DeliveryAdress string
	PickUpDate time.Time
	DeliveryDate time.Time
}
