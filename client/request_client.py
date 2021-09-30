import requests
import os


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