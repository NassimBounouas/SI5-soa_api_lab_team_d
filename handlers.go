package main

import (
	"encoding/json"
	"fmt"
	"net/http"
)

func ReceiveEvents(w http.ResponseWriter, r *http.Request) {
	/*order := Order{Meal: "Ramen", RestaurantAdress: "Lyang's restaurant", DeliveryAdress: "Polytech Nice Sophia"}
	js, err := json.Marshal(order)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	fmt.Println(r.Body)*/
	decoder := json.NewDecoder(r.Body)
	var event Event
	err := decoder.Decode(&event)
	if err != nil {
		http.Error(w,err.Error(), http.StatusInternalServerError)
		fmt.Println(err)
		return
	}
	//fmt.Println(event.Message)
	//w.Header().Set("Content-Type", "application/json")
	w.Write([]byte(ProcessEvent(event)))
}

func ProcessEvent(event Event) string {
	if event.Action == "Receive_order" {
		var order Order
		err := json.Unmarshal([]byte(event.Message), &order)
		if err != nil {
			fmt.Println(err)
			fmt.Println("Error while unmarshalling order")
			return ""
		}
		return "Order received, " + order.Meal + " in preparation"
	}
	return "unknown action"
}