# SI5-soa_api_lab_team_d_ordering_service

### Author
__Rudy MEERSMAN__
### Updated
__30/09/2018__

## Remarks
The Database is a json file named "Restaurant.json" where there's meals with theirs Restaurant
```json
{
  "plat" : [
    {
      "Id": 1,
      "Name": "Ramen",
      "Restaurant": "Lyianhg Restaurant",
      "Price" : "3.50"
    },
    {
      "Id": 2,
      "Name": "Pizza",
      "Restaurant": "Bar Roger",
      "Price" : "6.00"
    }
  ]
}
```

## Requirements
```
pip install flask
```

## API Usage

### Restaurant

* Get Restaurant who make the meal :: `[GET] http://127.0.0.1:5000/OrderMeal/<meal>`

Example :

> [GET] http://127.0.0.1:5000/OrderMeal/Ramen

```json
{
  "Order": {
    "Meal": "Ramen",
    "Price": "3.50",
    "Restaurant": "Lyianhg Restaurant"
  }
}
```

### Validation

* Return json of Order with unique ID for command :: `[GET] http://127.0.0.1:5000/ValidateOrder`

Example :

> [POST] http://127.0.0.1:5000/ValidateOrder/OK

>> Request Body 

```json
{
  "Meal": "Ramen",
  "Restaurant": "Lyianhg Restaurant",
  "Delivery_Address": "Templier",
  "Pick_Up_Date": "40",
  "Delivery_Date": "60"
  "Total Price" : "15.00€"
}
```

>>Answer

```json
{
  "Order": {
    "Command_Id": 62,
    "Delivery_Address": "Templier",
    "Delivery_Date": "60",
    "Meal": "Ramen",
    "Pick_Up_Date": "40",
    "Restaurant": "Lyianhg Restaurant",
    "Total Price": "15.00€"
  },
  "Status": "Accepted"
}
```

> [POST] http://127.0.0.1:5000/ValidateOrder/NO
>> Request Body 

```json
{
  "Meal": "Ramen",
  "Restaurant": "Lyianhg Restaurant",
  "Delivery_Address": "Templier",
  "Pick_Up_Date": "40",
  "Delivery_Date": "60"
  "Total Price" : "15.00€"
}
```

>>Answer

```json
{
  "Order": "none",
  "Status": "Canceled"
}
```

  
