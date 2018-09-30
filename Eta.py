from flask import Flask, request, jsonify
import random
app = Flask(__name__)
jsonFile = {}
jsonExist = False

__product__ = "Eta Service"
__author__ = "Duminy Gaetan"
__copyright__ = "Copyright 2018, Polytech Nice Sophia"
__credits__ = ["Duminy Gaetan"]
__license__ = "MIT"
__version__ = "1.0"
__maintainer__ = "Duminy Gaetan"
__email__ = "gaetan.duminy@etu.unice.fr"
__status__ = "development"


@app.route('/receiveOrder', methods=['POST'])
def receiveOrder():
    if request.is_json :
        global jsonFile, jsonExist
        jsonFile = request.get_json()
        jsonExist = True
        return 'JSON receive', 200
    else :
        return 'Not a JSON', 222
    
@app.route('/computeEta', methods=['GET'])
def computeEta():
    global jsonFile, jsonExist
    if jsonExist :
        time1 = random.randint(10, 20)
        time2 = time1 + random.randint(5, 15)
        return jsonify( Restaurant = jsonFile['Restaurant'],
                        Meal = jsonFile['Meal'],
                        DeliveryAddress = jsonFile['DeliveryAddress'],
                        PickUpDate = time1,
                        DeliveryDate = time2), 200
    else :
        return 'Send a JSON first', 200

@app.route('/')
def main():
    return "Welcome on Eta service"

if __name__ == '__main__':
    app.run()