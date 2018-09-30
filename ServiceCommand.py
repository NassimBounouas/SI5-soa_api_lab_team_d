from flask import Flask, request, jsonify
import json
import random

app = Flask(__name__)


@app.route('/OrderMeal/<string:meal>',methods = ['GET'])
def orderMeal(meal : str):
    resto = ""
    price = ""
    with open("Restaurant.json") as f:
        file = json.load(f)
    f.close()
    for i in file["plat"]:
        if i["Name"] == meal:
            resto = i["Restaurant"]
            price = i["Price"]
            break
    return jsonify( Order = {'Restaurant' : resto,
                    'Meal' : meal,
                    'Price' : price
    }
    )

@app.route('/ValidateOrder/<string:acceptation>',methods = ['POST'])
def validateOrder(acceptation : str):
    jsonMessage = request.get_json(force=True)
    if acceptation == "OK":
        data =  {
            'Command_Id' : random.randint(0,100),
            'Restaurant' : jsonMessage["Restaurant"],
            'Meal' : jsonMessage["Meal"],
            'Delivery_Address' : jsonMessage["Delivery_Address"],
            'Pick_Up_Date' : jsonMessage["Pick_Up_Date"],
            'Delivery_Date' : jsonMessage["Delivery_Date"],
            'Total Price' : jsonMessage["Total Price"]
    }
        return jsonify(
                    Order = data,
                    Status = "Accepted")
    else :
        return jsonify(
            Order = "none",
            Status = "Canceled"
        )

if __name__ == '__main__':
    app.run
