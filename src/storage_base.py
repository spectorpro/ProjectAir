from abc import ABC, abstractmethod
from typing import List, Optional
from src.aeroplane import Aeroplane

class StorageBase(ABC):
    @abstractmethod
    def add_aeroplane(self, aeroplane: Aeroplane) -> None:
        pass

    @abstractmethod
    def delete_aeroplane(self, identifier: str) -> bool:
        """Удаляет по уникальному идентификатору (например, icao24 или callsign)."""
        pass

    @abstractmethod
    def get_all(self) -> List[Aeroplane]:
        pass

    @abstractmethod
    def filter_by_country(self, country: str) -> List[Aeroplane]:
        pass

    @abstractmethod
    def clear(self) -> None:
        pass
