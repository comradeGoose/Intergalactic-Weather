from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates

router = APIRouter(
    prefix="/page",
    tags=["page"]
)

templates = Jinja2Templates(directory="static/html")


@router.get("/main")
def main(request: Request):
    return templates.TemplateResponse("canvas.html", {"request": request})


@router.get("/about")
def about(request: Request):
    return templates.TemplateResponse("canvas.html", {"request": request})


@router.get("/tokur")
def tokur(request: Request):
    return templates.TemplateResponse("canvas.html", {"request": request})


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
