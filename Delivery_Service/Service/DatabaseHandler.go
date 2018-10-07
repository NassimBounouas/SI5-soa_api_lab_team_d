package main

import (
	"database/sql"
	_ "github.com/go-sql-driver/mysql"
	"fmt"
	"log"
	"strconv"
)

func Read_to_delivers() []string {
	db, err := sql.Open("mysql", "root:root@tcp("+ Database +")/delivery_db?readTimeout=60s")
	if err != nil {
		fmt.Println(err)
		var string []string
		return strings
	}
	rows, err := db.Query("SELECT * FROM to_deliver_table")
	if err != nil {
		fmt.Println(err)
	}

	var delivers []string
	for rows.Next() {
		var id int
		var meal_name string
		var pickup_address string
		var delivery_address string
		err = rows.Scan(&id, &meal_name, &pickup_address, &delivery_address)
		if err != nil {
			fmt.Println(err)
			return delivers
		}
		fmt.Println("Delivery : ", id, " meal : ", meal_name, " from : ", pickup_address, " to : ", delivery_address)
		deliver := "Delivery : " + strconv.Itoa(id) + " meal : " + meal_name + " from : " + pickup_address + " to : " + delivery_address
		delivers = append(delivers, deliver)
	}

	db.Close()
	return delivers
}

func Add_to_deliver(order Order) {

	db, err := sql.Open("mysql", "root:root@tcp(" + Database + ")/delivery_db?readTimeout=60s")
	if err != nil {
		fmt.Println(err)
		return
	}
	stmt, err := db.Prepare("INSERT INTO to_deliver_table (meal_name, pickup_address, pickup_date, client, delivery_address) VALUES (?,?,?,?,?)")
	if err != nil {
		log.Fatal(err)
	}

	const MySQLTimeFormat = "2006-01-02 15:04:05"
	res, err := stmt.Exec(order.Meal, order.PickupAddress, order.PickUpDate.Format(MySQLTimeFormat), order.Client, order.DeliveryAdress)
	if err != nil {
		fmt.Println(err)
	}
	fmt.Println(res)
	db.Close()
}
