from pydantic import BaseModel


class WallpaperModel(BaseModel):
    url: str
    copyright: str
    copyrightlink: str
    location: dict
    cod: int

