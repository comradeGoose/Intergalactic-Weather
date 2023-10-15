from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
import requests
import json
import re

router = APIRouter(
    prefix="/wallpaper",
    tags=["wallpaper"]
)

# templates = Jinja2Templates(directory="templates")

def extract_state(input_string):
    pattern = r',\s(.+?)\s\('
    match = re.search(pattern, input_string)
    if match:
        state = match.group(1)
        return state
    else:
        return None

def extract_location(input_string):
    pattern = r',\s(.+),\s(.+)\s\('
    match = re.search(pattern, input_string)
    if match:
        location = f'{match.group(1)}, {match.group(2)}'
        return location
    else:
        return None
    
# test_strings = [ 
#     '--- , --- , dets , dets (123)', # gg
#     '--- , dets, dets (123)',
#     '--- , dets (123)' 
#     ]
# [print(extract_state(test)) for test in test_strings]

@router.post('')
def wallpaper(id: int = 0):
    # zh-CN
    data = requests.get(f'https://www.bing.com/HPImageArchive.aspx?format=js&idx={id}&n=1&mkt=ru').text
    copyright = json.loads(data)['images'][0]['copyright']
    copyrightlink = json.loads(data)['images'][0]['copyrightlink']
    url = json.loads(data)['images'][0]['urlbase']
    # location = extract_location(copyright)
    state = extract_state(copyright)
    return {
        'url': f'https://www.bing.com/{url}_1920x1080.jpg', 
        'copyright': copyright,
        'copyrightlink': copyrightlink,
        # 'location': location,
        'state': state
    }