from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
import requests
import json
from config import OPENWEATHERMAP_API_KEY

from datetime import datetime, timedelta
import pytz

router = APIRouter(
    prefix="/weather",
    tags=["weather"]
)


def seconds_to_date(seconds: int, timezone_offset: int) -> str:
    '''
    function converts an integer number of seconds and time offset into a string with the required date and time format
    '''
    dt = datetime.fromtimestamp(seconds, tz=pytz.UTC)
    custom_timezone = pytz.FixedOffset(timezone_offset // 60)
    dt = dt.astimezone(custom_timezone)
    formatted_date = dt.strftime("%b %d, %I:%M%p")
    return formatted_date


def date_to_seconds(date_str: str) -> int:
    '''
    function converts a date string to an integer number of seconds
    '''
    date_format = "%Y-%m-%d %H:%M:%S"
    date = datetime.strptime(date_str, date_format)
    seconds_since_epoch = (date - datetime(1970, 1, 1)).total_seconds()
    return int(seconds_since_epoch)


def get_horizon_side(deg: int) -> int:
    '''
    function returns one of the cardinal directions according to the entered angle
    '''
    directions = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE",
                  "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
    index = int((deg + 11.25) % 360 / 22.5)
    return directions[index]


@router.get('/now')
async def now(city: str = 'Tokur'):
    '''
    /now returns information about the weather in a given location
    '''

    try:
        response = requests.get(
            f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHERMAP_API_KEY}&units=metric')

        if response.status_code != 200:
            return {'cod': response.status_code, 'description': response.status_code}

        data = response.json()

        weather_data = {
            'weather': {
                'main': data['weather'][0]['main'],
                'description': data['weather'][0]['description'].capitalize(),
                'icon': data['weather'][0]['icon']
            },
            'base': data['base'],
            "main": {
                "temp": round(data['main']['temp']),
                "feels_like": round(data['main']['feels_like']),
                "temp_min": round(data['main']['temp_min']),
                "temp_max": round(data['main']['temp_max']),
                "pressure": round(data['main']['pressure']),
                "humidity": f"{round(data['main']['humidity'])}%",
                # "sea_level": round(data['main']['sea_level']),
                # "grnd_level": round(data['main']['grnd_level'])
            },
            "visibility": f"{data['visibility'] / 1000}km" if data['visibility'] >= 1000 else f"{data['visibility']}m",
            "wind": {
                "speed": round(data['wind']['speed'], 1),
                "deg": round(data["wind"]["deg"]),
                "horizon_side": get_horizon_side(round(data["wind"]["deg"])),
                "gust": round(data['wind']['gust'], 1)
            },
            "clouds": {
                "all": round(data['clouds']['all'])
            },
            "dt": seconds_to_date(data['dt'], data['timezone']),
            "sys": {
                "country": data['sys']['country'],
                "sunrise": seconds_to_date(data['sys']['sunrise'], data['timezone']),
                "sunset": seconds_to_date(data['sys']['sunset'], data['timezone'])
            },
            "timezone": data['timezone'],
            "id": data['id'],
            "name": data['name'],
            "cod": data['cod']
        }

        return weather_data

    except Exception as e:
        return {'cod': 500, 'description': str(e)}


@router.get('/forecast')
async def forecast(city: str = 'Tokur', count: int = 40):
    '''
    /forecast returns a forecast from count elements with a difference of 3 hours in a given location
    '''

    try:
        response = requests.get(
            f'https://api.openweathermap.org/data/2.5/forecast?q={city}&cnt={count}&appid={OPENWEATHERMAP_API_KEY}&units=metric')

        if response.status_code != 200:
            return {'cod': response.status_code, 'description': response.status_code}

        data = response.json()

        forecast_data = {
            'cod': data['cod'],
            'timezone': data['city']['timezone'],
            'sunrise': data['city']['sunrise'],
            'sunset': data['city']['sunset'],
            'list': []
        }

        for day in data['list']:
            forecast_data['list'].append({
                'date': date_to_seconds(day['dt_txt']),
                'pod': day['sys']['pod'],
                'visibility': f"{day['visibility'] / 1000}km" if day['visibility'] >= 1000 else f"{day['visibility']}m",
                'wind': day['wind']['speed'],
                'description': day['weather'][0]['description'].capitalize(),
                'temp': round(day['main']['temp']),
                'temp_min': round(day['main']['temp_min']),
                'temp_max': round(day['main']['temp_max']),
                'pop': day['pop'],
            })

            if day['pop'] == 0:
                continue

            if 'snow' in day:
                forecast_data['list'][-1]['snow'] = day['snow']['3h']

            if 'rain' in day:
                forecast_data['list'][-1]['rain'] = day['rain']['3h']

        return forecast_data

    except Exception as e:
        return {'cod': 500, 'description': str(e)}


@router.get('/direct')
async def direct(city: str = 'Tokur'):
    '''
    /direct returns . . .
    '''

    try:
        response = requests.get(
            f'https://api.openweathermap.org/geo/1.0/direct?q={city}&appid={OPENWEATHERMAP_API_KEY}')

        if response.status_code != 200:
            return {'cod': response.status_code, 'description': response.status_code}

        data = response.json()
        data[0]['cod'] = 200
        return data
    except Exception as e:
        return {'cod': 500, 'description': str(e)}


@router.get('/air_pollution')
async def air_pollution(city: str = 'Tokur'):
    '''
    /air_pollution returns . . .
    '''

    coordinates = await direct(city)

    if coordinates[0]['cod'] != 200:
        return {'cod': coordinates[0]['cod'], 'description': coordinates[0]['cod']}

    try:
        response = requests.get(
            f'http://api.openweathermap.org/data/2.5/air_pollution?lat=53.14064&lon=132.890274&appid={OPENWEATHERMAP_API_KEY}&units=metric')

        if response.status_code != 200:
            return {'cod': response.status_code, 'description': 'get air_pollution error'}

        data = response.json()

        return data

    except Exception as e:
        return {'cod': 500, 'description': str(e)}
