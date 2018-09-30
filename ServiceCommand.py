from flask import Flask, request, jsonify
import json
import random

app = Flask(__name__)


@app.route('/OrderMeal',methods = ['POST'])
def orderMeal():
    jsonMessage = request.get_json(force=True)
    resto = ""
    with open("Restaurant.json") as f:
        file = json.load(f)
    f.close()
    for i in file["plat"]:
        if i["Name"] == "Ramen":
            resto = i["Restaurant"]
            break
    return jsonify(
                    Restaurant = resto,
                    Meal = jsonMessage["Meal"])

@app.route('/ValidateOrder',methods = ['POST'])
def validateOrder():
    jsonMessage = request.get_json(force=True)
    return jsonify(
                   Restaurant = jsonMessage["Restaurant"],
                   Meal = jsonMessage["Meal"],
                   Delivery_Address = jsonMessage["Delivery_Address"],
                   Pick_Up_Date = jsonMessage["Pick_Up_Date"],
                   Delivery_Date = jsonMessage["Delivery_Date"],
                   Command_Id = random.randint(0,100))

if __name__ == '__main__':
    app.run()