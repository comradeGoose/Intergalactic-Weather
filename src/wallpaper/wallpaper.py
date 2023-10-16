from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
import requests
import json
import re

router = APIRouter(
    prefix="/wallpaper",
    tags=["wallpaper"]
)
 
def extract_location(input_string):
    # Используем регулярные выражения для поиска подстрок
    pattern1 = r'([^,]+,\s[^,]+)\s\('
    match1 = re.search(pattern1, input_string)
    substring1 = match1.group(1) if match1 else None

    pattern2 = r',\s([^,]+)\s\('
    match2 = re.search(pattern2, input_string)
    substring2 = match2.group(1) if match2 else None

    return [substring1[1:], substring2]

@router.post('')
def wallpaper(id: int = 0):
    # zh-CN
    data = requests.get(f'https://www.bing.com/HPImageArchive.aspx?format=js&idx={id}&n=1&mkt=ru').text
    copyright = json.loads(data)['images'][0]['copyright']
    copyrightlink = json.loads(data)['images'][0]['copyrightlink']
    url = json.loads(data)['images'][0]['urlbase']
    # location = extract_location(copyright)
    location = extract_location(copyright)
    return {
        'url': f'https://www.bing.com/{url}_1920x1080.jpg', 
        'copyright': copyright,
        'copyrightlink': copyrightlink,
        'location': location
    }