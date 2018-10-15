package main

import (
	"fmt"
	"github.com/confluentinc/confluent-kafka-go/kafka"
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
	//router := NewRouter()
    //log.Fatal(http.ListenAndServe(":8080", router))
	kafkaConsum()
}


func kafkaConsum() {
	c, err := kafka.NewConsumer(&kafka.ConfigMap{
		"bootstrap.servers":    "localhost:9092",
		"group.id":             1,
		"session.timeout.ms":   6000,
		"default.topic.config": kafka.ConfigMap{"auto.offset.reset": "earliest"}})

	if err != nil {
		fmt.Fprintf(os.Stderr, "Failed to create consumer: %s\n", err)
		os.Exit(1)
	}

	topics := []string{"test"}
	err = c.SubscribeTopics(topics, nil)

	run := true
	for run == true {
			ev := c.Poll(100)
			if ev == nil {
				continue
			}

			switch e := ev.(type) {
			case *kafka.Message:
				fmt.Printf("%% Message on %s:\n%s\n",
					e.TopicPartition, string(e.Value))
				if e.Headers != nil {
					fmt.Printf("%% Headers: %v\n", e.Headers)
				}
				ProcessEventKafka(e)
			case kafka.PartitionEOF:
				fmt.Printf("%% Reached %v\n", e)
			case kafka.Error:
				fmt.Fprintf(os.Stderr, "%% Error: %v\n", e)
				run = false
			default:
				fmt.Printf("Ignored %v\n", e)
			}
	}
}