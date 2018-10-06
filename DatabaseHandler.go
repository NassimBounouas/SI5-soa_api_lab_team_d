package main

import (
	"database/sql"
	_ "github.com/go-sql-driver/mysql"
	"fmt"
	"log"
)

func Read_to_delivers()  {
	db, err := sql.Open("mysql", "root:root@tcp(127.0.0.1:4014)/delivery_db")
	if err != nil {
		fmt.Println(err)
	}
	stmt, err := db.Prepare("SELECT * FROM to_deliver_table")
	if err != nil {
		fmt.Println(err)
	}
	res, err := stmt.Exec()
	if err != nil {
		fmt.Println(err)
	}
	fmt.Println(res)
	db.Close()
}

func Add_to_deliver(meal, pickup, delivery string) {

	db, err := sql.Open("mysql", "root:root@tcp(127.0.0.1:4014)/delivery_db")
	if err != nil {
		fmt.Println(err)
	}
	stmt, err := db.Prepare("INSERT INTO to_deliver_table (meal_name, pickup_address, delivery_address) VALUES (?,?,?)")
	if err != nil {
		log.Fatal(err)
	}

	res, err := stmt.Exec(meal, pickup, delivery)
	if err != nil {
		fmt.Println(err)
	}
	fmt.Println(res)
	db.Close()
}
