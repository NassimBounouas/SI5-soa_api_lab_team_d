from flask import Flask, request, jsonify
import random, datetime
app = Flask(__name__)

__product__ = "Eta Service"
__author__ = "Duminy Gaetan"
__copyright__ = "Copyright 2018, Polytech Nice Sophia"
__credits__ = ["Duminy Gaetan"]
__license__ = "MIT"
__version__ = "1.0"
__maintainer__ = "Duminy Gaetan"
__email__ = "gaetan.duminy@etu.unice.fr"
__status__ = "development"


@app.route('/receive_event', methods=['POST'])
def computeEta():
    if request.is_json :
        jsonFile = request.get_json()
        if jsonFile["Action"] == "compute_eta":
            message = jsonFile["Message"]
            time1 = random.randint(10, 20)
            time2 = time1 + random.randint(5, 15)
            date = datetime.datetime.now()
            data = { "Restaurant": message['Restaurant'],
                     "Meal": message['Meal'],
                     "Delivery_Address": message['Delivery_Address'],
                     "Pick_Up_Date": date + datetime.timedelta(minutes=time1),
                     "Delivery_Date": date + datetime.timedelta(minutes=time2)
                }
            return jsonify( Action = "validate_order",
                            Message = data), 200
                                
        else :
            return "Wrong service, the action here is compute_eta"
    else :
        return 'Not a JSON', 222

@app.route('/')
def main():
    return "Welcome on Eta service"

if __name__ == '__main__':
    app.run(host='0.0.0.0',port='5000')