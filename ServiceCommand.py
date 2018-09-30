from flask import Flask, request, jsonify
import random

app = Flask(__name__)
jsonMessage = {}

def whoFunction():
    if jsonMessage["EVENT"] == "ORDER_MEAL":
        return orderMeal()
    elif jsonMessage["EVENT"] == "VALIDATE_ORDER":
        return validateOrder()
    else:
        print("400 BAD REQUEST")
        return jsonify(jsonMessage)

def orderMeal():
    global jsonMessage
    f = open ("Restaurant.txt","r")
    line = f.readline()
    while line:
        name = line.split(" ")
        if jsonMessage["MEAL"] == name[0]:
            restaurant = name[1]
        line = f.readline()
    f.close()
    return jsonify(EVENT = jsonMessage["EVENT"],
                    RESTAURANT = restaurant,
                    MEAL = jsonMessage["MEAL"])

def validateOrder():
    global jsonMessage
    return jsonify(EVENT = jsonMessage["EVENT"],
                   RESTAURANT = jsonMessage["RESTAURANT"],
                   MEAL = jsonMessage["MEAL"],
                   DELIVERYADDRESS = jsonMessage["DELIVERYADDRESS"],
                   PICKUPDATE = jsonMessage["PICKUPDATE"],
                   DELIVERYDATE = jsonMessage["DELIVERYDATE"],
                   COMMANDID = random.randint(0,100))


@app.route('/',methods = ['GET','POST'])
def main():
    if request.method == 'POST' :
        global jsonMessage
        jsonMessage = request.get_json(force=True)
        return 'JSON posted'
    elif request.method == 'GET':
        return whoFunction()

if __name__ == '__main__':
    app.run(host='192.168.1.17')