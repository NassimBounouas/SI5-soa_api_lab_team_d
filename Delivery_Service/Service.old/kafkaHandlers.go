package main

import (
	"encoding/json"
	"fmt"
	"github.com/confluentinc/confluent-kafka-go/kafka"
)

func ProcessEventKafka(message *kafka.Message) {
	var event MessageEvent
	fmt.Println("Received : ", string(message.Value))
	err := json.Unmarshal(message.Value, &event)

	if err != nil {
		panic(err)
	}


	if event.Action == "Delivery_request" {
		var order Order
		err := json.Unmarshal([]byte(event.Message), &order)
		if err != nil {
			fmt.Println("Error while unmarshalling order", err)
		}
		//Add_to_deliver(order)
		fmt.Println("Order has been unmarshalled from kafka event")
		fmt.Println(order.PickUpDate)
		fmt.Println(order.PickupAddress)
		fmt.Println(order.DeliveryAdress)
		fmt.Println(order.Client)
		fmt.Println(order.Meal)
		//return generateResponseEvent("Your request has been accepted, your " + order.Meal + " will be picked up from " + order.PickupAddress + " at " + order.PickUpDate.Format(time.RFC3339) + " and delivered to " + order.DeliveryAdress)
	} else if event.Action == "List_request" {
		fmt.Println("Received a listing request")
		//return generateResponseEvent(strings.Join(Read_to_delivers(), ", "))
	} else {
		fmt.Println("The submitted action is unknown")
	}

}
