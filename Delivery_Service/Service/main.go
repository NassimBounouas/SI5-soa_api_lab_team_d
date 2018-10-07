package main

import (
	"fmt"
	"log"
	"net/http"
	"os"
)

var Database string
func main() {
	if(len(os.Getenv("DATABASE_DELIVERY")) != 0) {
		Database = os.Getenv("DATABASE_DELIVERY")
	} else {
		fmt.Println("Impossible to read database environment variable")
		os.Exit(1);
	}
	router := NewRouter()
    log.Fatal(http.ListenAndServe(":8080", router))
}