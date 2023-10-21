from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

from wallpaper.wallpaper import wallpaper
from weather.weather import now
from weather.weather import forecast
from weather.weather import air_pollution

from datetime import datetime


router = APIRouter(
    prefix="/page",
    tags=["page"]
)

templates = Jinja2Templates(directory="static/html")

TOKUR = {
    "url": "/static/image/2023-07-18_16-11_tokur.jpg",
    "copyright": "Центр ОВД (локатор), Токур, Амурская Область, Россия (© comrade goose)",
    "copyrightlink": "/page/tokur",
    "location": {
        "city": "Токур, Амурская Область, Россия",
        "state": "Амурская Область, Россия",
    }
}


@router.get("/main")
async def main(request: Request, id: int = 0):

    wallpaper_data = await wallpaper(id)

    if wallpaper_data['cod'] != 200:
        return RedirectResponse("/page/tokur")

    location = wallpaper_data['location']['city']

    weather_now = await now(location)

    if weather_now['cod'] != 200:
        location = wallpaper_data['location']['state']
        weather_now = await now(location)

    if weather_now['cod'] != 200:
        return RedirectResponse("/page/tokur")

    # weather_forecast = await forecast(location)

    # if weather_forecast['cod'] != 200:
    #     pass

    # weather_air_pollution = await air_pollution(location)
    # if weather_air_pollution['cod'] != 200:
    #     pass

    return templates.TemplateResponse("weather.html", {
        'request': request,
        'wallpaper_id': id,
        'year': datetime.now().year,
        'wallpaper_data': wallpaper_data,
        "weather_now": weather_now,
        "icon_weather_now": f'https://openweathermap.org/img/wn/{weather_now["weather"]["icon"]}@2x.png'
    })


@router.get("/about")
async def about(request: Request):

    wallpaper_data = await wallpaper()

    if wallpaper_data['cod'] != 200:
        return RedirectResponse("/page/tokur")

    location = wallpaper_data['location']['city']

    weather_now = await now(location)
    if weather_now['cod'] != 200:
        location = wallpaper_data['location']['state']
        weather_now = await now(location)

    if weather_now['cod'] != 200:
        return RedirectResponse("/page/tokur")

    return templates.TemplateResponse("canvas.html", {
        'request': request,
        'year': datetime.now().year,
        'wallpaper_data': wallpaper_data
    })


@router.get("/tokur")
def tokur(request: Request):
    return templates.TemplateResponse("tokur.html", {
        'request': request,
        'year': datetime.now().year,
        'wallpaper_data': TOKUR
    })

# @app.get("/")
# def main_page(request: Request, wallpaper_data=Depends(wallpaper)):
#   if wallpaper_data['cod'] != 500:
#     try:
#       weather_data = now(wallpaper_data['location']['city'])
#       if weather_data['cod'] != '404':
#           icon_current_weather = f'https://openweathermap.org/img/wn/{weather_data["weather"][0]["icon"]}@2x.png'
#           return templates.TemplateResponse("base.html", {
#               'request': request,
#               'wallpaper_data': wallpaper_data,
#               'weather_data': weather_data,
#               'icon_current_weather': icon_current_weather
#           })
#       else:
#           weather_data = now(wallpaper_data['location']['state'])
#           icon_current_weather = f'https://openweathermap.org/img/wn/{weather_data["weather"][0]["icon"]}@2x.png'
#           return templates.TemplateResponse("base.html", {
#               'request': request,
#               'wallpaper_data': wallpaper_data,
#               'weather_data': weather_data,
#               'icon_current_weather': icon_current_weather
#           })
#     except Exception as e:
#       print(str(e))
#       return templates.TemplateResponse("base.html", {
#           'request': request,
#           'wallpaper_data': wallpaper_data,
#           'weather_data': '',
#           'icon_current_weather': ''
#       })
#   else:
#     print('!!!!!!!!!!!!!!!!!!!!!')
#     return templates.TemplateResponse("base.html", {
#         'request': request,
#         'wallpaper_data': wallpaper_data,
#         'weather_data': '',
#         'icon_current_weather': ''
#     })
