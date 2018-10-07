package main

import "time"

type Order struct {
	Meal string
	Client string
	PickUpDate time.Time
}
