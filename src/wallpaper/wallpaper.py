from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
import requests
import json
import re

router = APIRouter(prefix="/wallpaper", tags=["wallpaper"])


def error(message: str = ""):
    return {
        "url": "/static/2023-07-18_16-11_tokur.jpg",
        "copyright": "- - - , Tokur, Amur Oblast, Russia (© comrade goose)",
        "copyrightlink": "",
        "location": {
            "city": "Tokur, Amur Oblast, Russia",
            "state": "Amur Oblast, Russia",
        },
        "cod": 500,
        "error": message,
    }


def extract_location(input_string):
    # Используем регулярные выражения для поиска подстрок
    pattern_city = r"([^,]+,\s[^,]+)\s\("
    match_city = re.search(pattern_city, input_string)
    city = match_city.group(1) if match_city else None

    pattern_state = r",\s([^,]+)\s\("
    match_state = re.search(pattern_state, input_string)
    state = match_state.group(1) if match_state else None

    return {"city": city[1:], "state": state}


@router.get("")
def wallpaper(id: int = 0):

    try:
        if type(id) != int:
            return error(f'type(id): {type(id)}')

        response = requests.get(f"https://www.bing.com/HPImageArchive.aspx?format=js&idx={id}&n=1&mkt=ru")
        if response.status_code != 200:
            return error(response.status_code)

        data = response.json()
        copyright = data["images"][0]["copyright"]
        copyrightlink = data["images"][0]["copyrightlink"]
        url = data["images"][0]["urlbase"]
        location = extract_location(copyright)

        return {
            "url": f"https://www.bing.com/{url}_1920x1080.jpg",
            "copyright": copyright,
            "copyrightlink": copyrightlink,
            "location": location,
            "cod": 200,
        }

    except Exception as e:
        print(str(e))
        return error(str(e))


