from flask import Flask, request, jsonify,g
import random
import pymysql
import configparser
import os
app = Flask(__name__)


def load_config():
    config_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "db.ini")
    if not os.path.exists(config_file):
        raise FileNotFoundError(config_file)
    app_config = configparser.ConfigParser()
    app_config.read(config_file)
    return app_config

@app.before_request
def before_request():
    configuration = load_config()["development"]
    try:
        g.db = pymysql.connect(host=configuration['host'],
                             port=int(configuration['port']),
                             user=configuration['user'],
                             password=configuration['pass'],
                             db=configuration['db'],
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor,
                             autocommit=True,
                             connect_timeout=60)
        g.connected = True
        print("Connected to Database.")
    except  pymysql.err.OperationalError:
        g.connected = False
        print("Cannot process request : unable to connect to the database. Maybe the `docker-compose` is not ready...")
        return jsonify({
            'status': 'KO',
            'message': "Cannot process request : unable to connect to the database. Maybe the `docker-compose` is not ready..."
        }), 500

@app.after_request
def after_request(response):
    if g.connected:
        g.db.close()
        print("Database closed.")
    g.connected = False
    return response

def orderMeal(jsonRecv):
    data = databaseReadRestaurant(jsonRecv["Meal"])
    return jsonify(
        Action = "compute_eta",
        Message = data
    )

def validateOrder(jsonRecv):
    ID = random.randint(0,100)
    data =  {
        'Command_Id' : ID,
        'Restaurant' : jsonRecv["Restaurant"],
        'Meal' : jsonRecv["Meal"],
        'Delivery_Address' : jsonRecv["Delivery_Address"],
        'Delivery_Date' : jsonRecv["Delivery_Date"]
    }
    databaseAddRecipe(jsonRecv)
    return jsonify(
        Message = data,
        Status = "Accepted")

def databaseAddRecipe(jsonRecv):
    cursor = g.db.cursor()
    sql = "INSERT INTO to_get_recipe(meal_name,restaurant_name,delivery_date,delivery_address,price) VALUES('%s','%s','%d','%s','%d')" %(jsonRecv["Meal"],jsonRecv["Restaurant"],jsonRecv["Delivery_Date"],jsonRecv["Delivery_Address"],jsonRecv["Price"])
    try:
        cursor.execute(sql)
        g.db.commit()
    except:
        g.db.rollback()
    return

def databaseReadRecipe(identifier):
    cursor = g.db.cursor()
    sql = ("SELECT * FROM to_get_recipe WHERE id=" + str(identifier))
    try:
        cursor.execute(sql)
    except:
        g.db.rollback()
    res = cursor.fetchall()
    if len(res) > 0:
        data = {
            'Command_Id' : res[0]['id'],
            'Restaurant' : res[0]['restaurant_name'],
            'Meal' : res[0]['meal_name'],
            'Delivery_Address' : res[0]['delivery_address'],
            'Delivery_Date' : res[0]['delivery_date'],
            'Price' : res[0]['price']
        }
    else:
        return jsonify(
        Message = "No Command in the database",
        Status = "Refused")

    return jsonify(
        Message = data,
        Status = "Accepted")

def databaseReadRestaurant(meal):
    cursor = g.db.cursor()
    sql = "SELECT * FROM to_get_restaurant WHERE meal_name=%s"
    try:
        cursor.execute(sql,meal)
    except:
        g.db.rollback()
    res = cursor.fetchall()
    return {
        'Restaurant' : res[0]['restaurant_name'],
        'Meal' : meal,
        'Price': res[0]['price']
    }

@app.route('/receive_event',methods = ['POST'])
def main():
    jsonMessage = request.get_json(force=True)
    if jsonMessage["Action"] == "validate_order":
        return validateOrder(jsonMessage["Message"])
    elif jsonMessage["Action"] == "order_meal":
        return orderMeal(jsonMessage["Message"])
    elif jsonMessage["Action"] == "validation_request":
        return databaseReadRecipe(jsonMessage["Message"]["Id"])
    else:
        return jsonify(
            error = "404 Not Found"
        )

if __name__ == '__main__':
    app.run(debug=True, host=
