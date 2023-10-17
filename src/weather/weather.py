from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
import requests
import json
from config import OPENWEATHERMAP_API_KEY

from typing import List
from weather.schemas import DirectModel

router = APIRouter(
    prefix="/weather",
    tags=["weather"]
)


@router.get('/now')
def now(city: str = 'Tokur'):

    try:
        response = requests.get(
            f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHERMAP_API_KEY}&units=metric')

        if response.status_code != 200:
            return {'cod': response.status_code, 'description': response.status_code}

        data = response.json()
        return data
    except Exception as e:
        print(str(e))
        return {'cod': 500, 'description': str(e)}


@router.get('/forecast')
def forecast(city: str = 'Tokur', count: int = 40):

    try:
        response = requests.get(
            f'https://api.openweathermap.org/data/2.5/forecast?q={city}&cnt={count}&appid={OPENWEATHERMAP_API_KEY}&units=metric')

        if response.status_code != 200:
            return {'cod': response.status_code, 'description': response.status_code}

        data = response.json()
        return data
    except Exception as e:
        print(str(e))
        return {'cod': 500, 'description': str(e)}


@router.get('/direct')
def direct(city: str = 'Tokur'):
    try:
        response = requests.get(
            f'https://api.openweathermap.org/geo/1.0/direct?q={city}&appid={OPENWEATHERMAP_API_KEY}')

        if response.status_code != 200:
            return {'cod': response.status_code, 'description': response.status_code}

        data = response.json()
        data[0]['cod'] = 200
        return data
    except Exception as e:
        print(str(e))
        return {'cod': 500, 'description': str(e)}


@router.get('/air_pollution')
def air_pollution(city: str = 'Tokur'):

    coordinates = direct(city)

    if coordinates[0]['cod'] != 200:
        try:
            # Default coordinates of Tokur:
            # lat: float = 53.14064, lon: float = 132.890274
            response = requests.get(
                f'http://api.openweathermap.org/data/2.5/air_pollution?lat=53.14064&lon=132.890274&appid={OPENWEATHERMAP_API_KEY}&units=metric')

            if response.status_code != 200:
                return {'cod': response.status_code, 'description': 'get air_pollution error'}

            data = response.json()
            return data

        except Exception as e:
            print(str(e))
            return {'cod': 500, 'description': str(e)}
    else:
        lat = coordinates[0]['lat']
        lon = coordinates[0]['lon']

        response = requests.get(
            f'http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={OPENWEATHERMAP_API_KEY}&units=metric')

        if response.status_code != 200:
            return {'cod': response.status_code, 'description': 'get air_pollution error'}

        data = response.json()
        return data
