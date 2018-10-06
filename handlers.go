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
			fmt.Println("Error while unmarshalling order", err)
			return generateErrorEvent("The submitted Order is malformed")
		}
		Add_to_deliver(order.Meal, order.RestaurantAdress, order.DeliveryAdress)
		return generateResponseEvent("Your request has been accepted, your " + order.Meal + " will be picked up at " + order.RestaurantAdress + " and delivered to " + order.DeliveryAdress)
	} else if event.Action == "List_request" {
		return generateResponseEvent(strings.Join(Read_to_delivers(), ", "))
	}
	return generateErrorEvent("The submitted action is unknown")
}

func generateErrorEvent(msg string) Event {
	var errorEvent Event
	errorEvent.Action = "Error"
	errorEvent.Message = msg
	return errorEvent
}

func generateResponseEvent(msg string) Event {
	var returnedEvent Event
	returnedEvent.Action = "Response"
	returnedEvent.Message = msg
	return returnedEvent
}