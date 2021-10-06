import requests
import os


def call_json_req():
    scoring_uri = "http://127.0.0.1:5000/api_group_a/echo"
    headers = {'Content-Type': 'application/json'}

    rawdata = {"df_input": "001", }
    raw_str = json.dumps(rawdata)
    print("input_data json = {}".format(raw_str))
    response = requests.post(scoring_uri, data=raw_str, headers=headers)
    print(response.status_code)
    print(response.elapsed)
    dic_respon = response.json()

    print(dic_respon.keys())
    print("response json {}".format(dic_respon))

    print()
    return dic_respon


def test_multiple_file():
    """
    test multiple file format upload and download
    :return:
    """
    #url = "http://localhost:5000/upload_files"

    url = "http://localhost:5000/api_group_a/upload_files"

    root_folder = os.path.join('.', 'sample_files')
    filename_1 = os.path.join(root_folder, '01.jpg')
    filename_2 = os.path.join(root_folder, '02.png')
    filename_3 = os.path.join(root_folder, 'test.json')

    raw_user_info = {"name":"Tom"}

    files=[('file',   ('01.jpg',open(filename_1,'rb'), 'image/jpeg')),
           ('file_2', ('02.png', open(filename_2, 'rb'), 'image/png')),
           ('cfg', ('test.json', open(filename_3,'rb'), 'application/json'),)     ]

    headers = {
        'accept': 'application/json',
    }

    response = requests.post(url, headers=headers, data=raw_user_info, files=files)
    response.json()


if __name__ == '__main__':
    test_multiple_file()
