from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

from datetime import datetime

from wallpaper.wallpaper import wallpaper
from weather.weather import now

from wallpaper.wallpaper import router as router_wallpaper
from weather.weather import router as router_weather
from pages.router import router as router_pages

app = FastAPI(
    title='Intergalactic Weather',
    version='0.0.1 ~ 4'
)
app.mount("/static", StaticFiles(directory="static"), name="static")

# @app.get('/')
# def hello(request: Request):
#     return {'client_host': request.client.host, 'client_port': request.client.port}

templates = Jinja2Templates(directory="static/html")


@app.get("/")
def redirect():
    return RedirectResponse("/page/main")


@app.get("/page")
def redirect():
    return RedirectResponse("/page/main")

@app.get("/page/")
def redirect():
    return RedirectResponse("/page/main")


app.include_router(router_wallpaper)
app.include_router(router_weather)
app.include_router(router_pages)

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
