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
import urllib.parse

from urllib.parse import urlparse
from os.path import isfile
from os.path import splitext
from os.path import join as joinpath
from dotenv import load_dotenv
from os import listdir


def createparser():
    parser = argparse.ArgumentParser()
    parser.add_argument('time', nargs='?', default=10)
    return parser


def save_image(url, path_save):
    filename = str(uuid.uuid4())
    urllib.request.urlretrieve(url, f'./{path_save}/{filename}.png')


def fetch_spacex_last_launch(url):
    response = requests.get(url)
    response.raise_for_status()
    info = response.json()['links']
    for key, value in info.items():
        if key == 'flickr_images':
            for url_image_spacex in value:
                save_image(url_image_spacex, images_path_nasa)


def get_image_url_nasa(image_name, image_date):
    payload = {'api_key': api_key_nasa}
    response = requests.get(
        f'https://api.nasa.gov/EPIC/archive/natural/{image_date}/png/{image_name}.png',
        params=payload)
    response.raise_for_status()
    return response.url


def save_nasa_image(nasa_epic, image_name,image_date):
        format_url_nasa(nasa_epic)
        url_epic_image_nasa = get_image_url_nasa(image_name, image_date)
        save_image(url_epic_image_nasa, images_path_nasa)

def format_url_nasa(nasa_epic):
    for name in nasa_epic:
        image_date = format_nasa_epic_date(name)
        image_name = get_nasa_epic_image(name)
        return image_name, image_date

def fetch_nasa_epic_images(url, api_key):
        payload = {'api_key': api_key}
        response = requests.get(url, params=payload)
        response.raise_for_status()
        nasa_epic = response.json()
        for name in nasa_epic:
            for key, value in name.items():
                if key == "date":
                    value = datetime.datetime.fromisoformat(value)
                    image_date = value.strftime('%Y/%m/%d')
            for key, value in name.items():
                if key == "image":
                    image_name = value
            save_nasa_image(nasa_epic, image_name, image_date)

def fetch_nasa_apod_images(url_apod_nasa, api_key_nasa, path_save):
    payload = {'api_key': api_key_nasa,
               'count': 30}
    response = requests.get(
        url_apod_nasa,
        params=payload)
    response.raise_for_status()
    nasa_url = response.json()
    for url in nasa_url:
        for key, value in url.items():
            if key == 'hdurl':
                url = urlparse(value)
                split_url = (splitext(url.path))
                ext_image = split_url[1]
                filename = str(uuid.uuid4())
                urllib.request.urlretrieve(value, f'./{path_save}/{filename}{ext_image}')


if __name__ == '__main__':

    load_dotenv()
    api_key_nasa = os.environ['API_KEY_NASA']
    api_key_telegram = os.environ['API_KEY_TELEGRAM']
    chat_id = os.environ['CHAT_ID_TELEGRAM']

    images_path_nasa = 'images_nasa'
    os.makedirs(images_path_nasa, exist_ok=True)

    url_epic_nasa = 'https://api.nasa.gov/EPIC/api/natural'
    url_apod_nasa = 'https://api.nasa.gov/planetary/apod'
    fetch_nasa_apod_images(url_apod_nasa, api_key_nasa, images_path_nasa)
    fetch_nasa_epic_images(url_epic_nasa, api_key_nasa)

    parser = createparser()
    namespace = parser.parse_args()
    sleep_time = namespace.time

    url_spacex = 'https://api.spacexdata.com/v3/launches/65'
    fetch_spacex_last_launch(url_spacex)

    path = "./images_nasa"
    for image in listdir(path):
        if isfile(joinpath(path, image)):
            bot = telegram.Bot(token=api_key_telegram)
            time.sleep(sleep_time)
            with open(f'./images_nasa/{image}', 'rb') as file:
                bot.send_document(chat_id=chat_id, document=file)
