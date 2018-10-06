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
	//w.Header().Set("Content-Type", "plain/text")
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
		Add_to_deliver(order.Meal, order.RestaurantAdress, order.DeliveryAdress)
		return "Your request has been accepted, your " + order.Meal + " will be picked up at " + order.RestaurantAdress + " and delivered to " + order.DeliveryAdress
	} else if event.Action == "List_request" {
		fmt.Println(strings.Join(Read_to_delivers(), ","))
			return strings.Join(Read_to_delivers(), ",")
	}
	return "unknown action"
}