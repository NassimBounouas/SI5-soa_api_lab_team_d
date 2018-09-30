package main

import (
	"encoding/json"
	"fmt"
	"net/http"
)

func ReceiveEvents(w http.ResponseWriter, r *http.Request) {
	decoder := json.NewDecoder(r.Body)
	var event Event
	err := decoder.Decode(&event)
	if err != nil {
		http.Error(w,err.Error(), http.StatusInternalServerError)
		fmt.Println(err)
		return
	}
	w.Write([]byte(ProcessEvent(event)))
}

func ProcessEvent(event Event) string {
	if event.Action == "Delivery_request" {
		var order Order
		err := json.Unmarshal([]byte(event.Message), &order)
		if err != nil {
			fmt.Println(err)
			fmt.Println("Error while unmarshalling order")
			return ""
		}
		return "Your request has been accepted, your " + order.Meal + " will be picked up at " + order.RestaurantAdress + " and delivered to " + order.DeliveryAdress
	}
	return "unknown action"
}