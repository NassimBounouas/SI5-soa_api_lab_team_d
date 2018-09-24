package main

import (
	"encoding/json"
    "fmt"
    "html"
    "log"
    "net/http"
    "github.com/gorilla/mux"
)

func main() {
	router := mux.NewRouter().StrictSlash(true)
	router.HandleFunc("/", Index)
	router.HandleFunc("/receive_events", ReceiveEvents)
    log.Fatal(http.ListenAndServe(":8080", router))
}

func Index(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintf(w, "Hello, %q", html.EscapeString(r.URL.Path))
}

func ReceiveEvents(w http.ResponseWriter, r *http.Request) {
	order := Order{Meal: "Ramen", RestaurantAdress: "Lyang's restaurant", DeliveryAdress: "Polytech Nice Sophia"}
	json.NewEncoder(w).Encode(order)
}
