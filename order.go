package main

import "time"

type Order struct {
	Meal string
	PickupAddress string
	PickUpDate time.Time
	Client string
	DeliveryAdress string
}
