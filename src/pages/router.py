from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates

from wallpaper.wallpaper import wallpaper
from weather.weather import weather

router = APIRouter(
    prefix="/weather",
    tags=["weather"]
)

templates = Jinja2Templates(directory="static/html")


# @router.get("")
# def get_search_page(request: Request, url_wallpaper=Depends(wallpaper)):
#     print(url_wallpaper)
#     return templates.TemplateResponse("weather.html", {"request": request, "url_wallpaper": url_wallpaper})

@router.get("/")
def main_page(request: Request, wallpaper_data=Depends(wallpaper)):
  try:
    weather_data = weather(wallpaper_data['location'][0])
    if weather_data['cod'] != '404':
      icon_current_weather = f'https://openweathermap.org/img/wn/{weather_data["weather"][0]["icon"]}@2x.png'
      return templates.TemplateResponse("weather.html", {
        'request': request, 
        'wallpaper_data': wallpaper_data, 
        'weather_data': weather_data,
        'icon_current_weather': icon_current_weather
        })
    else:
      weather_data = weather(wallpaper_data['location'][1])
      icon_current_weather = f'https://openweathermap.org/img/wn/{weather_data["weather"][0]["icon"]}@2x.png'
      return templates.TemplateResponse("weather.html", {
        'request': request, 
        'wallpaper_data': wallpaper_data, 
        'weather_data': weather_data,
        'icon_current_weather': icon_current_weather
        })
    
  except Exception as e:
    print(str(e))
    return templates.TemplateResponse("weather.html", {
      'request': request, 
      'wallpaper_data': 'error', 
      'weather_data': 'error',
      'icon_current_weather': 'error'
      })