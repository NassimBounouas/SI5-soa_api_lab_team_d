package main

import (
	"encoding/json"
	"fmt"
	"net/http"
)

func ReceiveEvents(w http.ResponseWriter, r *http.Request) {
	order := Order{Meal: "Ramen", RestaurantAdress: "Lyang's restaurant", DeliveryAdress: "Polytech Nice Sophia"}
	js, err := json.Marshal(order)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	fmt.Println(r.Body)
	decoder := json.NewDecoder(r.Body)
	var event Event
	err = decoder.Decode(&event)
	if err != nil {
		http.Error(w,err.Error(), http.StatusInternalServerError)
		return
	}
	fmt.Println(event)
	w.Header().Set("Content-Type", "application/json")
	w.Write(js)
}