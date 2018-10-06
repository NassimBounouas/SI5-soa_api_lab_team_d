package main

import (
	"encoding/json"
	"fmt"
	"net/http"
	"strings"
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
	event = ProcessEvent(event)
	marshalledEvent, err := json.Marshal(event)
	if err != nil {
		http.Error(w,err.Error(), http.StatusInternalServerError)
		fmt.Println(err)
		return
	}
	w.Write([]byte(marshalledEvent))
}

func ProcessEvent(event Event) Event {
	if event.Action == "Delivery_request" {
		var order Order
		err := json.Unmarshal([]byte(event.Message), &order)
		if err != nil {
			fmt.Println(err)
			fmt.Println("Error while unmarshalling order")
			var errorEvent Event
			errorEvent.Action = "Error"
			errorEvent.Message = "The submitted Order is malformed"
			return errorEvent
		}
		Add_to_deliver(order.Meal, order.RestaurantAdress, order.DeliveryAdress)
		var returnedEvent Event
		returnedEvent.Action = "Response"
		returnedEvent.Message = "Your request has been accepted, your " + order.Meal + " will be picked up at " + order.RestaurantAdress + " and delivered to " + order.DeliveryAdress
		return returnedEvent
	} else if event.Action == "List_request" {
		var returnedEvent Event
		returnedEvent.Action = "Response"
		returnedEvent.Message = strings.Join(Read_to_delivers(), ", ")
		return returnedEvent
	}
	var errorEvent Event
	errorEvent.Action = "Error"
	errorEvent.Message = "The submitted action is unknown"
	return errorEvent
}