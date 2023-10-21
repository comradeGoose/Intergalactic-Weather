from pydantic import BaseModel


class DirectModel(BaseModel):
    name: str
    local_names: dict
    lat: float
    lon: float
    country: str
    state: str


class WeatherModel(BaseModel):
    pass


class ForecastModel(BaseModel):
    pass
