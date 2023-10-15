from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
import requests
import json
from config import OPENWEATHERMAP_API_KEY

router = APIRouter(
    prefix="/weather",
    tags=["weather"]
)

# templates = Jinja2Templates(directory="templates")

@router.post('/')
def weather(city: str = 'Tokur'):

    try:
        response = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHERMAP_API_KEY}&units=metric')
        data = response.json()
        return data
    except Exception as e:
        print(str(e))
        return 'Произошла ошибка при получении информации о погоде.'
