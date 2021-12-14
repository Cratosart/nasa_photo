import sys
import requests
import os
import datetime
import urllib.request
import uuid
import urllib
import telegram
import time
import argparse

from os.path import isfile
from os.path import join as joinpath
from dotenv import load_dotenv
from os import listdir


def createparser():
    parser = argparse.ArgumentParser()
    parser.add_argument('time', nargs='?', default=86400)
    return parser


def create_nasa_epic_requests(url, api_key):
    payload = {'api_key': api_key}
    response = requests.get(url_epic_nasa, params=payload)
    response.raise_for_status()
    return response


def formatting_nasa_epic_date(nasa_epic):
    for key, value in nasa_epic.items():
        if key == "date":
            value = datetime.datetime.fromisoformat(value)
            date_image = value.strftime('%Y/%m/%d')
            return date_image


def getting_nasa_epic_image(nasa_epic):
    for key, value in nasa_epic.items():
        if key == "image":
            image_name = value
            return image_name


def save_image(url, path_save):
    filename = str(uuid.uuid4())
    urllib.request.urlretrieve(url, f'./{path_save}/{filename}.png')

def spacex_requests(url):
    payload={}
    headers = {}
    response = requests.request("GET", url_spacex, headers=headers, data=payload)
    return response

def fetch_spacex_last_launch (info):
    for key, value in info.items():
        if key == 'flickr_images':
            for url_image_spacex in value:
                save_image(url_image_spacex,images_path_nasa)


if __name__ == '__main__':
    load_dotenv()
    api_key_nasa = os.environ['API_KEY_NASA']
    api_key_telegram = os.environ['API_KEY_TELEGRAM']
    chat_id = os.environ['CHAT_ID_TELEGRAM']

    images_path_nasa = 'images_nasa'
    os.makedirs(images_path_nasa, exist_ok=True)


    url_epic_nasa = 'https://api.nasa.gov/EPIC/api/natural'

    nasa_epic = create_nasa_epic_requests(url_epic_nasa, api_key_nasa).json()
    for name in nasa_epic:
        image_date = formatting_nasa_epic_date(name)
        image_name = getting_nasa_epic_image(name)
        payload = {'api_key': api_key_nasa}
        response = requests.get(f'https://api.nasa.gov/EPIC/archive/natural/{image_date}/png/{image_name}.png', params=payload)
        url_epic_image_nasa = response.url
        save_image(url_epic_image_nasa, images_path_nasa)

    parser = createparser()
    namespace = parser.parse_args()
    sleep_time = namespace.time

    url_spacex = 'https://api.spacexdata.com/v3/launches/65'
    response = spacex_requests(url_spacex)
    info = response.json()['links']
    i = fetch_spacex_last_launch(info)


    path = "./images_nasa"
    for image in listdir(path):
        if isfile(joinpath(path, image)):
            bot = telegram.Bot(token=api_key_telegram)
            time.sleep(sleep_time)
            with open(f'./images_nasa/{image}', 'rb') as file:
                bot.send_document(chat_id=chat_id,document=file)

