from flask import Flask

from flasgger import Swagger
from flask_cors import CORS

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
    #"openapi":"3.0.0",
    'uiversion':3
}

CORS(app)
Swagger(app)


def bytes_to_cv2image(imgdata):
    cv2img = cv2.cvtColor(np.array(Image.open(BytesIO(imgdata))), cv2.COLOR_RGB2BGR)
    return cv2img

a =  """Upload files in to server
    Retrieve node list
    ---
    requestBody:
        content:
            multipart/form-data:
                schema:
                    type: object
                    properties:
                        filename:
                            type: array
                            items:
                                type: string
                                format: binary

    responses:
        401:
            description: Unauthorized error
        200:
            description: Retrieve node list
            examples:
                node-list: [{"id":26},{"id":44}]
    """
"""Upload files in to server
Retrieve node list
---
requestBody:
    content:
        multipart/form-data:
            schema:
                type: object
                properties:
                    fileName:
                        type: file
                        format: binary
responses:
    401:
        description: Unauthorized error
    200:
        description: Retrieve node list
        examples:
            node-list: [{"id":26},{"id":44}]
"""

@app.route("/upload_files", methods=[ 'POST'])
def upload_files():
    """
    This API let's you train word embeddings
    Call this api passing your file and get the word embeddings.
    ---
    consumes:
        - multipart/form-data
    parameters:
        - name: file
          in: formData
          type: file
          required: true
          description: The file to upload.
        - name: cfg
          in: formData
          type: file
          required: true
          description: The cfg json file to upload.
              {
                   "Hello":"abcd",
                   "lst":[1,2,3,4],
                   "lst2":[[1,2],[4,5],[5,6]]
              }
          example: {"Hello":"abcd"}

        - name: dict_data
          in: formData
          type: string
          required: true
          description: The json string to upload.
          example: "Hello"

    responses:
        500:
            description: ERROR Failed!
        200:
            description: INFO Success!
    """
    dict_json = request.get_json()

    for file_key in request.files:
        file_item = request.files[file_key]
        print(file_item.filename)
        str_path = secure_filename(file_item.filename)
        file_item.save(os.path.join(app.config['UPLOAD_FOLDER'], str_path))
    img_data = request.files['file']
    img_data.seek(0)
    cvimg = bytes_to_cv2image(img_data.read())

    cvimg = cv2.cvtColor(cvimg, cv2.COLOR_BGR2GRAY)  # 轉為單通道灰階
    cvimg = cv2.cvtColor(cvimg, cv2.COLOR_GRAY2BGR)  # 單通道灰階轉為三通道灰階
    cv2.imwrite('output.jpg', cvimg)
    str_base64 = cv2image_to_base64(cvimg)

    return jsonify({"filename": str_path, "r_base64_str": str_base64, "pic_idx": pic_idx})


@app.route("/echo", methods=['POST'])
def echo_print():
    """
      Get All Node List
      Retrieve node list
      ---
      tags:
        - Node APIs
      produces: application/json,
      parameters:
      - name: name
        in: path
        type: string
        required: true
        example: hello
      - name: node_id
        in: path
        type: string
        required: true
        example: not hello

      responses:
        401:
          description: Unauthorized error
        200:
          description: Retrieve node list
          examples:
            node-list: [{"id":26},{"id":44}]
    """
    if request.method == 'POST':
        dict_json = request.get_json()
        print(dict_json)
    return jsonify({"echo": dict_json})


@app.route("/image_to_file", methods=['POST'])
def image_to_file():
    global pic_idx
    if request.method == 'POST':
        dict_json = request.get_json()
        _root_folder = "/home/node-red/deryannhuang/temp"
        _root_folder = "."
        str_base64 = dict_json['base64_str']
        str_path = os.path.join(_root_folder, "uuid_{}.jpg".format(pic_idx))
        base64_to_file(str_base64, str_path)
        cvimg = base64_to_cv2image(str_base64)
        cvimg = cv2.cvtColor(cvimg, cv2.COLOR_BGR2GRAY)  # 轉為單通道灰階
        cvimg = cv2.cvtColor(cvimg, cv2.COLOR_GRAY2BGR)  # 單通道灰階轉為三通道灰階
        str_base64 = cv2image_to_base64(cvimg)
        pic_idx += 1
        return jsonify({"filename": str_path, "r_base64_str": str_base64, "pic_idx": pic_idx})


@app.route("/inc")
def inc():
    """
      Get add one into counter
      Retrieve counter value
      ---
      tags:
        - Node APIs
      produces: application/json,
      responses:
        401:
          description: Unauthorized error
        200:
          description: Retrieve counter value
          schema:
              type: string
              example: "1"
    """
    global g_inc
    g_inc += 1
    return "{}".format(g_inc)


@app.route("/")
def hello():
    a = "[start]\t{}\n".format(datetime.datetime.now())
    import pkg_resources
    installed_packages = [(d.project_name, d.version) for d in pkg_resources.working_set]
    out_string = '\n'.join("{} \t {}".format(item[0], item[1]) for item in installed_packages)
    b = "[end]\t{}\n".format(datetime.datetime.now())
    return a + "Flask inside Docker!!" + '\n pip list \n' + out_string + '\n' + b


@app.route("/time")
def print_time():
    return "{}".format(datetime.datetime.now())


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))

    app.run(debug=True, host='0.0.0.0', port=port)

