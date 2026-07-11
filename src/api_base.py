from abc import ABC, abstractmethod
import requests

class BaseApiClient(ABC):
    @abstractmethod
    def get_country_bbox(self, country_name: str):
        """Получить bounding box страны (координаты)."""
        pass

    @abstractmethod
    def get_aeroplanes_in_area(self, south: float, west: float, north: float, east: float):
        """Получить самолёты в прямоугольнике координат."""
        pass
