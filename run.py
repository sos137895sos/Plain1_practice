from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
import os

MONGO_HOST = os.environ.get('MONGO_HOST', '127.0.0.1:27017')

app = Flask(__name__)
CORS(app)
client = MongoClient(MONGO_HOST)


@app.route('/')
def status():
    return 'vue_api ok'


@app.route('/add_info', methods=['POST'])
def add_info_json():
    col = client['vue']['info']

    data = request.get_json()

    col.insert_one(data)

    name = data.get('name')
    age = data.get('age')
    gender = data.get('gender')
    detail = data.get('detail')

    # Add CORS headers
    response = jsonify({'message': 'Success'})
    response.headers.add('Access-Control-Allow-Origin',
                         'http://localhost:8081')
    response.headers.add('Access-Control-Allow-Methods', 'POST')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')

    # 檢查是否有空值
    if not all([name, age, gender, detail]):
        return jsonify({'error': f'All fields must be provided.\n{request.form}'}), 400

    # 在這裡可以進一步處理接收到的數據
    return jsonify({'message': 'Information added successfully.'})


@app.route('/a', methods=['*'])
def add():
    data = request.form.get('data')


if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0')
