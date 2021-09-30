import os
from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

api_group_a = Blueprint('APIGroupA', __name__)

# Get current path
path = os.getcwd()
# file Upload
UPLOAD_FOLDER = os.path.join(path, 'uploads')

# Make directory if uploads is not exists
if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

custom_config = dict()
custom_config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

import os
import datetime
import cv2
import base64

import numpy as np
from io import BytesIO
from PIL import Image
from werkzeug.utils import secure_filename

from flask import request
from flask import jsonify


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


g_inc = 0
pic_idx = 0


def bytes_to_cv2image(imgdata):
    cv2img = cv2.cvtColor(np.array(Image.open(BytesIO(imgdata))), cv2.COLOR_RGB2BGR)
    return cv2img


@api_group_a.route("/upload_files", methods=['GET', 'POST'])
def upload_files():
    if request.method == 'POST':
        dict_json = request.get_json()

        for file_key in request.files:
            file_item = request.files[file_key]
            print(file_item.filename)
            str_path = secure_filename(file_item.filename)
            file_item.save(os.path.join(custom_config['UPLOAD_FOLDER'], str_path))

        img_data = request.files['file']
        img_data.seek(0)
        cv_img = bytes_to_cv2image(img_data.read())

        cv_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)  # 轉為單通道灰階
        cv_img = cv2.cvtColor(cv_img, cv2.COLOR_GRAY2BGR)  # 單通道灰階轉為三通道灰階
        cv2.imwrite('output.jpg', cv_img)
        str_base64 = cv2image_to_base64(cv_img)

    return jsonify({"filename": str_path, "r_base64_str": str_base64, "pic_idx": pic_idx})


@api_group_a.route("/echo", methods=['GET', 'POST'])
def echo_print():
    if request.method == 'POST':
        dict_json = request.get_json()
        print(dict_json)
    return jsonify({"echo": dict_json})


@api_group_a.route("/image_to_file", methods=['GET', 'POST'])
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


@api_group_a.route("/inc")
def inc():
    global g_inc
    g_inc += 1
    return "{}".format(g_inc)


@api_group_a.route("/")
def hello():
    a = "[start]\t{}\n".format(datetime.datetime.now())
    import pkg_resources
    installed_packages = [(d.project_name, d.version) for d in pkg_resources.working_set]
    out_string = '\n'.join("{} \t {}".format(item[0], item[1]) for item in installed_packages)
    b = "[end]\t{}\n".format(datetime.datetime.now())
    return a + "Flask inside Docker!!" + '\n pip list \n' + out_string + '\n' + b


@api_group_a.route("/time")
def print_time():
    return "{}".format(datetime.datetime.now())
