package main

import (
	"database/sql"
	_ "github.com/go-sql-driver/mysql"
	"fmt"
	"log"
	"time"
)

func Register_an_order(date time.Time, order Order) {

	db, err := sql.Open("mysql", "root:root@tcp(" + Database + ")/chinese_restaurant_db?readTimeout=60s")
	if err != nil {
		fmt.Println(err)
		return
	}
	stmt, err := db.Prepare("INSERT INTO to_prepare_table (order_time, pickup_date, client, meal_name) VALUES (?,?,?,?)")
	if err != nil {
		log.Fatal(err)
	}
	const MySQLTimeFormat = "2006-01-02 15:04:05"
	res, err := stmt.Exec(date.Format(MySQLTimeFormat), order.PickUpDate.Format(MySQLTimeFormat), order.Client, order.Meal)
	if err != nil {
		fmt.Println(err)
	}
	fmt.Println(res)
	db.Close()
}
