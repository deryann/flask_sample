from flask import Flask

from flasgger import Swagger
from flask_cors import CORS

import json
import os
import datetime
import cv2
import base64

import numpy as np
from io import BytesIO
from PIL import Image
from werkzeug.utils import secure_filename


def base64_to_file(base64_string, filename):
    with open(filename, "wb") as fh:
        fh.write(base64.decodebytes(base64_string.encode('utf-8')))


def cv2image_to_base64(cv2img):
    retval, buffer_img = cv2.imencode('.jpg', cv2img)
    base64_str = base64.b64encode(buffer_img)
    str_a = base64_str.decode('utf-8')
    return str_a


def base64_to_cv2image(base64_string):
    imgdata = base64.b64decode(base64_string)
    cv2img = cv2.cvtColor(np.array(Image.open(BytesIO(imgdata))), cv2.COLOR_RGB2BGR)
    return cv2img


app = Flask(__name__)

from flask import request
from flask import jsonify

g_inc = 0
pic_idx = 0

# Get current path
path = os.getcwd()
# file Upload
UPLOAD_FOLDER = os.path.join(path, 'uploads')

# Make directory if uploads is not exists
if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config['SWAGGER'] = {
    "title": "deryann API ",
    "description": "My API",
    "version": "1.0.2",
    "termsOfService": "",
    "hide_top_bar": True,
    'uiversion': 2
}


def bytes_to_cv2image(imgdata):
    cv2img = cv2.cvtColor(np.array(Image.open(BytesIO(imgdata))), cv2.COLOR_RGB2BGR)
    return cv2img


@app.route("/upload_file", methods=['POST'])
def upload_file():
    """
    Upload one file
    ---
    tags:
        - File Upload Example API
    consumes:
        - multipart/form-data
    parameters:
        - in: formData
          name: file_input
          type: file
          required: true
          description: The file to upload.

    responses:
        500:
            description: ERROR Failed!
        200:
            description: INFO Success!
    """

    file_item = request.files['file_input']
    print(file_item.filename)
    s_name = secure_filename(file_item.filename)
    str_path = os.path.join(app.config['UPLOAD_FOLDER'], s_name)
    file_item.save(str_path)
    file_item.seek(0)
    return jsonify({"filepath": str_path, })


@app.route("/upload_3_files", methods=['POST'])
def upload_files():
    """
    上傳 3 個檔案的 API
    ---
    tags:
        - File Upload Example API
    consumes:
        - multipart/form-data
    parameters:
        - name: file_01
          in: formData
          type: file
          required: true
          description: The file 01 to upload.
        - name: file_02
          in: formData
          type: file
          required: true
          description: The file 02 to upload.
        - name: cfg_file
          in: formData
          type: file
          required: true
          description: The file 03 to upload by json format.

    responses:
        500:
            description: ERROR Failed!
        200:
            description: INFO Success!
    """
    lst_file_path_in_server = []
    for file_key in ['file_01', 'file_02', 'cfg_file']:
        file_item = request.files[file_key]
        print(file_item.filename)
        s_name = secure_filename(file_item.filename)
        str_path = os.path.join(app.config['UPLOAD_FOLDER'], s_name)
        file_item.save(str_path)
        file_item.seek(0)
        lst_file_path_in_server.append(str_path)

    # extra to parse the cfg_file from json to dictionary
    file_item = request.files['cfg_file']
    dic_loaded = json.load(file_item)
    print(dic_loaded)

    return jsonify({"filepathes": lst_file_path_in_server, "cfg_loaded": dic_loaded})


#
@app.route("/gray_image", methods=['POST'])
def gary_image():
    """
    Gray your jpeg image
    return gray_image base64
    ---
    tags:
        - File Upload Example API
    consumes:
        - multipart/form-data
    parameters:
        - in: formData
          name: file_input
          type: file
          required: true
          description: The file will become gray.

    responses:
        500:
            description: ERROR Failed!
        200:
            description: INFO Success!

    """
    if request.method == 'POST':
        img_data = request.files['file_input']

        cvimg = bytes_to_cv2image(img_data.read())

        cvimg = cv2.cvtColor(cvimg, cv2.COLOR_BGR2GRAY)  # 轉為單通道灰階
        cvimg = cv2.cvtColor(cvimg, cv2.COLOR_GRAY2BGR)  # 單通道灰階轉為三通道灰階
        cv2.imwrite('output.jpg', cvimg)
        str_base64 = cv2image_to_base64(cvimg)
    return jsonify({"str_base64": str_base64})


#
#
@app.route("/echo", methods=['POST'])
def echo_print():
    """
    Get json dictionary input
    Return echo data with "echo" key
    ---
    tags:
      - JSON POST API
    produces: application/json,
    parameters:
        - in: body
          name: input_json
          description: input json data
          schema:
              type: object
              example: {"a": "777", "b": "999" }

    responses:
        401:
            description: Unauthorized error
        200:
            description: Retrieve echo data
            example: {"echo": {"a": "777", "b": "999" }}
    """
    if request.method == 'POST':
        dict_json = request.get_json()
        print(dict_json)
    return jsonify({"echo": dict_json})


@app.route("/add_function", methods=['POST'])
def add_function():
    """
    Get a, b
    Return sum of a, b
    ---
    tags:
      - JSON POST API
    produces: application/json,
    parameters:
      - in: body
        name: two_number
        description: prepare 2 numbers for add function.
        schema:
            type: object
            required:
              - a
              - b
            properties:
                a:
                    type: int
                    example: 3
                b:
                    type: int
                    example: 4

    responses:
        401:
          description: Unauthorized error
        200:
          description: Retrieve sum value
          schema:
            type: object
            required:
              - sum
            properties:
              sum:
                type: integer
                description: sum of 2 numbers.
                example: 7

    """
    if request.method == 'POST':
        dict_json = request.get_json()
        n_sum = dict_json['a'] + dict_json['b']
    return jsonify({"sum": n_sum})


@app.route("/inc")
def inc():
    """
      Get add one into counter
      Retrieve counter value
      ---
      tags:
        - Get APIs
      produces: application/json,
      responses:
        401:
          description: Unauthorized error
        200:
          description: Retrieve counter value

    """
    global g_inc
    g_inc += 1
    return "{}".format(g_inc)


@app.route("/")
def hello():
    """
    Get all pip list packages
    Retrieve all python package and version
    ---
    tags:
      - Get APIs
    responses:
      401:
        description: Unauthorized error
      200:
        description: Retrieve all python package and version
    """

    a = "[start]\t{}\n".format(datetime.datetime.now())
    import pkg_resources
    installed_packages = [(d.project_name, d.version) for d in pkg_resources.working_set]
    out_string = '\n'.join("{} \t {}".format(item[0], item[1]) for item in installed_packages)
    b = "[end]\t{}\n".format(datetime.datetime.now())
    return a + "Flask inside Docker!!" + '\n pip list \n' + out_string + '\n' + b


@app.route("/time")
def print_time():
    """
    Get system time
    Retrieve system time from server
    ---
    tags:
      - Get APIs
    responses:
      401:
        description: Unauthorized error
      200:
        description: Retrieve system time string
    """
    return "{}".format(datetime.datetime.now())


CORS(app)
Swagger(app)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))

    app.run(debug=True, host='0.0.0.0', port=port)
