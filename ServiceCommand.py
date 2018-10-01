from flask import Flask, request, jsonify
import json
import random

app = Flask(__name__)


def orderMeal(jsonRecv):
    resto = ""
    price = ""
    with open("Restaurant.json") as f:
        file = json.load(f)
    f.close()
    for i in file["Plat"]:
        if i["Name"] == jsonRecv["Meal"]:
            resto = i["Restaurant"]
            break
    data = {
        'Restaurant' : resto,
        'Meal' : jsonRecv["Meal"]
    }
    return jsonify(
        Action = "compute_eta",
        Message = data
    )

def validateOrder(jsonMessage):
    data =  {
        'Command_Id' : random.randint(0,100),
        'Restaurant' : jsonMessage["Restaurant"],
        'Meal' : jsonMessage["Meal"],
        'Delivery_Address' : jsonMessage["Delivery_Address"],
        'Delivery_Date' : jsonMessage["Delivery_Date"]
    }
    return jsonify(
        Action = data,
        Status = "Accepted")

@app.route('/receive_event',methods = ['POST'])
def main():
    jsonMessage = request.get_json(force=True)
    if jsonMessage["Action"] == "validate_order":
        return validateOrder(jsonMessage["Message"])
    elif jsonMessage["Action"] == "order_meal":
        return orderMeal(jsonMessage["Message"])
    else:
        return jsonify(
            error = "404 Not Found"
        )

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
