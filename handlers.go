package main

import (
	"encoding/json"
	"fmt"
	"net/http"
	"time"
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
	if event.Action == "Receive_order" {
		var order Order
		err := json.Unmarshal([]byte(event.Message), &order)
		if err != nil {
			fmt.Println("Error while unmarshalling order", err)
			return generateErrorEvent("The submitted Order is malformed")
		}
		fmt.Println(order)
		Register_an_order(time.Now(), order)
		return generateResponseEvent("Order received, " + order.Meal + " in preparation to be picked up at : " + order.PickUpDate.Format(time.RFC3339))
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