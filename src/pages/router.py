from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates

from wallpaper.wallpaper import wallpaper

router = APIRouter(
    prefix="/pages",
    tags=["Pages"]
)

templates = Jinja2Templates(directory="templates/html")


@router.get("")
def get_search_page(request: Request, url_wallpaper=Depends(wallpaper)):
    print(url_wallpaper)
    return templates.TemplateResponse("base.html", {"request": request, "url_wallpaper": url_wallpaper})
