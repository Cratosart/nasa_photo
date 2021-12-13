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
    parser.add_argument('time', nargs='?', default=10)
    return parser


def create_nasa_epic_requests(url):
    payload = {}
    headers = {}
    response = requests.request("GET", url_epic_nasa, headers=headers, data=payload)
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


if __name__ == '__main__':
    load_dotenv()
    api_key_nasa = os.environ['API_KEY_NASA']
    api_key_telegram = os.environ['API_KEY_TELEGRAM']
    chat_id = os.environ['CHAT_ID_TELEGRAM']
    images_path_nasa = 'images_nasa'
    if not os.path.exists(images_path_nasa):
        os.mkdir(images_path_nasa)

    url_epic_nasa = 'https://api.nasa.gov/EPIC/api/natural?api_key=cz0rECf7cwW5n90a51pe01jDNPuPAlgM9Wtp0KWa'

    nasa_epic = create_nasa_epic_requests(url_epic_nasa).json()
    for name in nasa_epic:
        image_date = formatting_nasa_epic_date(name)
        image_name = getting_nasa_epic_image(name)
        url_epic_image_nasa = f'https://api.nasa.gov/EPIC/archive/natural/{image_date}/png/{image_name}.png?api_key={api_key_nasa} '
        save_image(url_epic_image_nasa, images_path_nasa)

    parser = createparser()
    namespace = parser.parse_args()
    sleep_time = namespace.time

    path = "./images_nasa"
    for image in listdir(path):
        if isfile(joinpath(path, image)):
            bot = telegram.Bot(token=api_key_telegram)
            time.sleep(sleep_time)
            with open(f'./images_nasa/{image}', 'rb') as file:
                bot.send_document(chat_id=chat_id,document=file)
            # bot.send_document(chat_id=chat_id,
            #                   document=open(f'./images_nasa/{image}', 'rb'),close=close(f'./images_nasa/{image}'))
