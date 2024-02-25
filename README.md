# Plain1_practice

一．建立簡易flask能在網頁顯示內容
    建立一個py檔並寫上需要的code
二．建立vue資料夾並寫出一個vue表單
    生成一个Vue.js项目的文件夹通常需要以下步骤：

    1.安装Node.js和npm：首先确保您的计算机上安装了Node.js。您可以从官方网站下载并安装Node.js，它还会自动安装npm（Node包管理器）。
    2.安装Vue CLI：Vue CLI是一个官方提供的用于快速搭建Vue.js项目的命令行工具。您可以使用以下命令全局安装Vue CLI：
        npm install -g @vue/cli

    3.创建新的Vue项目：安装完Vue CLI后，您可以使用vue create命令来创建一个新的Vue项目。在命令行中，转到您想要创建项目的目录，然后运行以下命令：
        vue create my-vue-project

        其中my-vue-project是您希望项目文件夹的名称。然后Vue CLI会提示您选择一些配置选项，例如是否使用默认配置或手动配置，以及您想要使用的附加功能。

    4.进入项目文件夹：创建项目后，进入项目文件夹：
        cd my-vue-project

    5.启动开发服务器：进入项目文件夹后，您可以使用以下命令启动Vue开发服务器：
         npm run serve

    这将启动一个开发服务器，并在浏览器中打开您的Vue.js应用程序。

    这样，您就可以成功生成一个Vue.js项目的文件夹，并开始开发您的Vue.js应用程序了。

三．用docker建立mongo資料庫以及flask api伺服器的容器
    要使用 Docker Compose 建立包含 MongoDB 数据库和 Flask API 服务器的应用程序，您可以按照以下步骤操作：

    1.创建 Dockerfile: 首先，您需要为 Flask 应用程序创建一个 Dockerfile。在您的 Flask 项目根目录下创建一个名为 Dockerfile 的文件，内容类似于：

    Dockerfile

        FROM python:3.9-slim

        WORKDIR /app

        COPY requirements.txt requirements.txt
        RUN pip install -r requirements.txt

        COPY . .

        CMD ["python", "app.py"]

    这个 Dockerfile 假设您的 Flask 应用程序的入口文件是 app.py，并且您已经在项目中定义了一个 requirements.txt 文件来管理 Python 依赖。

    2.创建 docker-compose.yml 文件: 在您的项目根目录下创建一个名为 docker-compose.yml 的文件，用于定义您的 Docker Compose 配置。内容类似于：
    yml   
        version: '3'

        services:
            mongodb:
                image: mongo
                container_name: mongodb
                ports:
                - "27017:27017"

        flask-api:
            build: .
            container_name: flask-api
            ports:
             - "5000:5000"
            depends_on:
            - mongodb

    这个配置文件定义了两个服务：mongodb 和 flask-api。mongodb 服务使用了官方的 MongoDB 镜像，flask-api 服务则使用了当前目录下的 Dockerfile 构建。flask-api 服务依赖于 mongodb 服务，因为 Flask API 服务器需要连接到 MongoDB 数据库。

    3.编写 Flask API 代码: 编写您的 Flask API 代码，并确保在 app.py 中包含了连接 MongoDB 数据库的逻辑。

    4.构建和运行: 执行以下命令，使用 Docker Compose 构建和运行您的应用程序：

        css

            docker-compose up --build

    这将会构建和启动您的两个服务：MongoDB 数据库和 Flask API 服务器。

    现在，您已经使用 Docker Compose 成功建立了一个包含 MongoDB 数据库和 Flask API 服务器的应用程序。您可以通过访问 http://localhost:5000 来访问您的 Flask API。
四．flask新增一個api以處理vue傳送過來的表單內容並將內容存近mongo資料庫
```python
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

```