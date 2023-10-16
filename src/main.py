from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from datetime import datetime

from wallpaper.wallpaper import wallpaper
from weather.weather import weather

from wallpaper.wallpaper import router as router_wallpaper
from weather.weather import router as router_weather
# from pages.router import router as router_pages

app = FastAPI(
    title='Intergalactic Weather'
)

app.mount("/static", StaticFiles(directory="static"), name="static")

# @app.get('/')
# def hello(request: Request):
#     return {'client_host': request.client.host, 'client_port': request.client.port}

templates = Jinja2Templates(directory="static/html")

@app.get("/")
def main_page(request: Request, wallpaper_data=Depends(wallpaper)):
  
  try:
    weather_data = weather(wallpaper_data['location'][0])
    if weather_data['cod'] != '404':
      icon_current_weather = f'https://openweathermap.org/img/wn/{weather_data["weather"][0]["icon"]}@2x.png'
      return templates.TemplateResponse("base.html", {
        'request': request, 
        'wallpaper_data': wallpaper_data, 
        'weather_data': weather_data,
        'icon_current_weather': icon_current_weather
        })
    else:
      weather_data = weather(wallpaper_data['location'][1])
      icon_current_weather = f'https://openweathermap.org/img/wn/{weather_data["weather"][0]["icon"]}@2x.png'
      return templates.TemplateResponse("base.html", {
        'request': request, 
        'wallpaper_data': wallpaper_data, 
        'weather_data': weather_data,
        'icon_current_weather': icon_current_weather
        })
    
  except Exception as e:
    print(str(e))
    return templates.TemplateResponse("base.html", {
      'request': request, 
      'wallpaper_data': 'error', 
      'weather_data': 'error',
      'icon_current_weather': 'error'
      })

app.include_router(router_wallpaper)
app.include_router(router_weather)
# app.include_router(router_pages)

origins = [
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
                   "Authorization"],
)
