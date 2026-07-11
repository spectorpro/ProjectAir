import requests
from src.api_base import BaseApiClient

class OpenskyApiClient(BaseApiClient):
    BASE_URL = "https://opensky-network.org/api/states/all"

    def __init__(self):
        self.session = requests.Session()

    def get_country_bbox(self, country_name: str):
        raise NotImplementedError("Nominatim отвечает за получение boundingbox.")

    def get_aeroplanes_in_area(self, south: float, west: float, north: float, east: float):
        params = {
            "lamin": south,
            "lomin": west,
            "lamax": north,
            "lomax": east,
        }
        resp = self.session.get(self.BASE_URL, params=params, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        states = data.get("states", [])
        return states
