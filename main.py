import requests
import os
import datetime
import urllib.request
import uuid
import urllib
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ['API_KEY_NASA']


def nasa_epic_requests(url):
    payload = {}
    headers = {}
    response = requests.request("GET", url_epic_nasa, headers=headers, data=payload)
    return response


def nasa_epic_date(nasa_epic):
    for key, value in nasa_epic.items():
        if key == "date":
            value = datetime.datetime.fromisoformat(value)
            date_image = value.strftime('%Y/%m/%d')
            return date_image


def nasa_epic_image(nasa_epic):
    for key, value in nasa_epic.items():
        if key == "image":
            image_name = value
            return image_name


def image_save(url, path_save):
    filename = str(uuid.uuid4())
    urllib.request.urlretrieve(url, f'./{path_save}/{filename}.png')


images_path_nasa = 'images_nasa'
if not os.path.exists(images_path_nasa):
    os.mkdir(images_path_nasa)

url_epic_nasa = 'https://api.nasa.gov/EPIC/api/natural?api_key=cz0rECf7cwW5n90a51pe01jDNPuPAlgM9Wtp0KWa'

nasa_epic = nasa_epic_requests(url_epic_nasa).json()
for name in nasa_epic:
    image_date = nasa_epic_date(name)
    image_name = nasa_epic_image(name)
    url_epic_image_nasa = f'https://api.nasa.gov/EPIC/archive/natural/{image_date}/png/{image_name}.png?api_key={api_key}'
    image_save(url_epic_image_nasa, images_path_nasa)
