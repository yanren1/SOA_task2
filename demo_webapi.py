from flask import Flask, request, jsonify

app = Flask(__name__)

# 一个简单的数据存储字典，用于演示
data_store = {}

@app.route('/')
def hello():
    return "Welcome to my Web API!"


# 通过GET请求获取数据
@app.route('/api/data/find', methods=['GET'])
def get_data():
    key = request.args.get('key')
    if key in data_store:
        return jsonify({key: data_store[key]})
    else:
        return jsonify({"error": "Key not found"}), 404


# 通过GET请求添加数据
@app.route('/api/data/add', methods=['GET'])
def add_data():
    # text = request.args.get('text')
    key = request.args.get('key')
    value = request.args.get('value')
    if key and value:
        data_store[key] = value
        return jsonify({"message": "Data added successfully"})
    else:
        return jsonify({"error": "Invalid data"}), 400


if __name__ == "__main__":
    app.run()
