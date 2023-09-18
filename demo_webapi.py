from flask import Flask, request, jsonify
from zeep import Client

client = Client('http://localhost:8000/?wsdl')
app = Flask(__name__)

# python dict for demo
data_store = {}

@app.route('/')
def hello():
    return "Welcome to my Web API!"


# use GET request to search
@app.route('/searchData', methods=['GET'])
def searchData():
    key = request.args.get('key')
    if key in data_store:
        return jsonify({key: data_store[key]})
    else:
        return jsonify({"error": "Key not found"}), 404


# use GET to add data
@app.route('/addData', methods=['POST'])
def add_data():
    # text = request.args.get('text')
    key = request.args.get('key')
    value = request.args.get('value')
    if key and value:
        if key in list(data_store.keys()):
            data_store[key].append(value)
        else:
            data_store[key] = [value]
        return jsonify({"message": "Data added successfully"})
    else:
        return jsonify({"error": "Invalid data"}), 400

@app.route('/getSum', methods=['GET'])
def getSum():
    # text = request.args.get('text')
    key = request.args.get('key')
    print(data_store.keys())
    # try:
    if key in list(data_store.keys()):
        sum = 0
        for i in data_store[key]:
                sum = client.service.add(sum, float(i))[0]
                # sum += float(i)
            # except:
            #     return jsonify({"message": "Data Error, please check data type."})
        return jsonify({"message": f"Sum of key {key} is {sum}."})

    else:
        return jsonify({"message": f"Key {key} not found."})
    #
    # except:
    #     return jsonify({"error": "Invalid data"}), 400


if __name__ == "__main__":
    app.run()
