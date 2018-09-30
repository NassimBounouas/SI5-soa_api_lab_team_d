# SI5_soa_api_lab_team_d_menu_service

### Author
Nikita ROUSSEAU
### Updated
11:52 30/09/2018

## Remarks

The database is mocked before each request.

Only `Read` Operations are available.

## Server Startup

```bash
export FLASK_APP=app.py
export FLASK_ENV=development

flask run --host 0.0.0.0 --port 5000

# * Serving Flask application
```

## API Usage

### Categories

* List categories :: [GET] http://127.0.0.1:5000`/categories`

Example :

> [GET] http://127.0.0.1:5000`/categories`

```json
{
    "categories": [
        {
            "id": 1,
            "name": "Japonais",
            "region": "Asie"
        },
        {
            "id": 2,
            "name": "Chinois",
            "region": "Asie"
        }
    ],
    "status": "OK"
}
```

### Meals

* List meals by category :: [GET] http://127.0.0.1:5000`/meals/<category>`

Example :

> [GET] http://127.0.0.1:5000/meals/Japonais

```json
{
    "meals": [
        {
            "category": "Japonais",
            "id": 1,
            "is_menu": false,
            "name": "Sushis saumon",
            "price": 3.9
        },
        {
            "category": "Japonais",
            "id": 2,
            "is_menu": false,
            "name": "Sushis saumon épicé",
            "price": 4.5
        },
        {
            "category": "Japonais",
            "id": 3,
            "is_menu": false,
            "name": "Sushis saumon mariné au jus de yuzu et ses herbes",
            "price": 4.8
        },
        {
            "category": "Japonais",
            "id": 5,
            "is_menu": true,
            "name": "Plateau 1 - 8 pièces",
            "price": 13.9
        }
    ],
    "status": "OK"
}
```

> Note :
> The category must be passed by the category name
