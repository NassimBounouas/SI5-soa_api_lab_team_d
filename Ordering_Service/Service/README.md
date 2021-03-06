# SI5-soa_api_lab_team_d_ordering_service

### Author
 * __Nikita ROUSSEAU__
 * __Rudy MEERSMAN__
### Updated
__06/11/2018__

## Requirements

- Python 3.6.x
- Dependencies :
  * PyMySQL
  * kafka-python

### Install Dependencies

```bash
pip install --trusted-host pypi.python.org -r requirements.txt
```

## Server Startup

```bash
python3 app.py <production|development>
INFO:root:Starting...
INFO:root:Ready !
INFO:root:Serving application in `development` environment
```

## Service Usage

### Create an order

Usage :

> Listening `ordering` topic
```json
{
  "action": "RESTAURANT_ORDER_REQUEST",
  "message": {
    "request": 1664,
    "id_meal": 33,
    "id_code": 0,
    "id_restaurant" : 11,
    "client_name" : "Victor",
    "client_address" : "les Templiers"
  }
}
```

> Response on `ordering`:

```json
{
  "action": "ORDER_CREATED",
  "message": {
    "status": "OK",
    "request": 1664,
    "order": {
      "id_order": 11,
      "id_meal": 33,
      "id_restaurant": 11,
      "id_code": 0,
      "client_name": "Victor",
      "client_address": "les Templiers",
      "status": "Created"
    }
  }
}
```

### Validate an order

Usage :

> Listening `ordering` topic
```json
{
  "action": "VALIDATE_ORDER_REQUEST",
  "message": {
    "request": 1665,
    "id_order": 11,
    "id_meal": 33,
    "id_restaurant" : 11
  }
}
```

> Response on `ordering`:

```json
{
  "action": "ORDER_ACCEPTED",
  "message": {
    "status": "OK",
    "request": 1665,
    "order": {
      "id_order": 11,
      "status": "Accepted"
    }
  }
}
```

> Response on `restaurant`:

```json
{
  "action": "PREPARE_ORDER",
  "message": {
    "status": "OK",
    "request": 1665,
    "order": {
      "id_order": 11,
      "id_meal": 33,
      "id_restaurant": 11
    }
  }
}
```

### Get list of order

Usage :

> Listening `restaurant` topic
```json
{
  "action" : "ORDER_LIST_REQUEST",
  "message" : {
    "status" : "OK",
    "request" : 10,
    "id_restaurant" : 10
    }
}
```

> Response on `restaurant`:

```json
{
  "action" : "ORDER_LIST_RESPONSE",
  "message" : {
    "status": "OK",
    "request": 10,
    "List" : [
              {
                "id_meal": 13,
                "id_order": 11
              },
              {
                "id_meal": 18,
                "id_order": 12
              }
             ]
            }
}
```

### Notify order when finished

Usage:

> Listening on `restaurant`:
```json
{
    "action": "NOTIFY_DELIVERY_RESPONSE" ,
    "message": {
        "request":42,
        "id_order":11
    }
}

```
Response : `Service is not generating any response`