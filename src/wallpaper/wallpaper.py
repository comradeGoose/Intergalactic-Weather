from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
import requests
import json
import re
from wallpaper.schemas import WallpaperModel

router = APIRouter(prefix="/wallpaper", tags=["wallpaper"])


def tokur(cod: int = 200, message: str = ""):
    return {
        "url": "/static/image/2023-07-18_16-11_tokur.jpg",
        "copyright": "Центр ОВД (локатор), Токур, Амурская Область, Россия (© comrade goose)",
        "copyrightlink": "/page/tokur",
        "location": {
            "city": "Токур, Амурская Область, Россия",
            "state": "Амурская Область, Россия",
        },
        "cod": cod,
        "message": message,
    }


def extract_location(input_string: str) -> {"city": str, "state": str}:
    '''
    returns a dictionary with two substrings of the input string
    '''
    pattern_city = r"([^,]+,\s[^,]+)\s\("
    match_city = re.search(pattern_city, input_string)
    city = match_city.group(1) if match_city else None
    pattern_state = r",\s([^,]+)\s\("
    match_state = re.search(pattern_state, input_string)
    state = match_state.group(1) if match_state else None
    return {"city": city[1:], "state": state}


@router.get("")
async def wallpaper(id: int = 0) -> WallpaperModel:
    '''
    returns information about the current Bing Wallpaper
    '''

    try:
        if type(id) != int:
            return {'cod': 500, 'description': f'type(id): {type(id)}'}

        response = requests.get(
            f"https://www.bing.com/HPImageArchive.aspx?format=js&idx={id}&n=1&mkt=ru")
        if response.status_code != 200:
            return {'cod': response.status_code, 'description': response.status_code}

        data = response.json()
        copyright = data["images"][0]["copyright"]
        copyrightlink = data["images"][0]["copyrightlink"]
        url = data["images"][0]["urlbase"]
        location = extract_location(copyright)

        return {
            "url": f"https://www.bing.com{url}_1920x1080.jpg",
            "copyright": copyright,
            "copyrightlink": copyrightlink,
            "location": location,
            "cod": 200,
        }

    except Exception as e:
        return {'cod': 500, 'description': str(e)}
