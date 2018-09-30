package main

import (
	"net/http"
)

type Route struct {
	Name string
	Method string
	Pattern string
	HandlerFunc http.HandlerFunc
}

type Routes []Route

var routes = Routes{
	Route{
		"receive_event",
		"POST",
		"/receive_event",
		ReceiveEvents,
	},
}