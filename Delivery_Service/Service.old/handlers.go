package main

import (
	"encoding/json"
	"fmt"
	"net/http"
	"strings"
	"time"
)

func ReceiveEvents(w http.ResponseWriter, r *http.Request) {
	decoder := json.NewDecoder(r.Body)
	var event MessageEvent
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

func ProcessEvent(event MessageEvent) MessageEvent {
	if event.Action == "Delivery_request" {
		var order Order
		err := json.Unmarshal([]byte(event.Message), &order)
		if err != nil {
			fmt.Println("Error while unmarshalling order", err)
			return generateErrorEvent("The submitted Order is malformed")
		}
		Add_to_deliver(order)
		return generateResponseEvent("Your request has been accepted, your " + order.Meal + " will be picked up from " + order.PickupAddress + " at " + order.PickUpDate.Format(time.RFC3339) + " and delivered to " + order.DeliveryAdress)
	} else if event.Action == "List_request" {
		return generateResponseEvent(strings.Join(Read_to_delivers(), ", "))
	}
	return generateErrorEvent("The submitted action is unknown")
}

func generateErrorEvent(msg string) MessageEvent {
	var errorEvent MessageEvent
	errorEvent.Action = "Error"
	errorEvent.Message = msg
	return errorEvent
}

func generateResponseEvent(msg string) MessageEvent {
	var returnedEvent MessageEvent
	returnedEvent.Action = "Response"
	returnedEvent.Message = msg
	return returnedEvent
}