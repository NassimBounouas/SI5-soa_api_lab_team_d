package main

import (
	"encoding/json"
	"net/http"
)

func ReceiveEvents(w http.ResponseWriter, r *http.Request) {
	order := Order{Meal: "Ramen", RestaurantAdress: "Lyang's restaurant", DeliveryAdress: "Polytech Nice Sophia"}
	js, err := json.Marshal(order)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	w.Header().Set("Content-Type", "application/json")
	w.Write(js)
}