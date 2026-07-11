import requests
from src.api_base import BaseApiClient

class NominatimApiClient(BaseApiClient):
    BASE_URL = "https://nominatim.openstreetmap.org/search"

    def __init__(self, user_agent: str = "course_project"):
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": user_agent})

    def get_country_bbox(self, country_name: str):
        params = {
            "q": country_name,
            "format": "json",
            "limit": 1,
            "countrycodes": None,
        }
        resp = self.session.get(self.BASE_URL, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        if not data:
            raise ValueError(f"Страна '{country_name}' не найдена.")
        result = data[0]
        # boundingbox: [south, north, west, east]
        bbox = result.get("boundingbox")
        if not bbox or len(bbox) != 4:
            raise ValueError(f"Некорректный boundingbox для страны '{country_name}'.")
        south, north, west, east = map(float, bbox)
        return south, west, north, east

    def get_aeroplanes_in_area(self, south: float, west: float, north: float, east: float):
        # Этот метод здесь не используется напрямую, но нужен для соответствия интерфейсу.
        # Реальная логика получения самолётов — в OpenskyApiClient.
        raise NotImplementedError("Используйте OpenskyApiClient для получения самолётов.")
