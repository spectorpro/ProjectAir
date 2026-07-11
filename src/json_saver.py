import json
from pathlib import Path
from storage_base import StorageBase
from aeroplane import Aeroplane

class JSONSaver(StorageBase):
    def __init__(self, filepath: str = "aeroplanes.json"):
        self.filepath = Path(filepath)
        self._ensure_file()

    def _ensure_file(self):
        if not self.filepath.exists():
            self.filepath.write_text("[]", encoding="utf-8")

    def _load_data(self) -> list:
        try:
            text = self.filepath.read_text(encoding="utf-8")
            data = json.loads(text)
            if not isinstance(data, list):
                return []
            return data
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def _save_data(self, data: list) -> None:
        with self.filepath.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def add_aeroplane(self, aeroplane: Aeroplane) -> None:
        data = self._load_data()
        entry = {
            "icao24": aeroplane.icao24,
            "callsign": aeroplane.callsign,
            "origin_country": aeroplane.origin_country,
            "velocity": aeroplane.velocity,
            "geo_altitude": aeroplane.geo_altitude,
            "longitude": aeroplane.longitude,
            "latitude": aeroplane.latitude,
        }
        # Удаляем None для чистоты JSON
        entry = {k: v for k, v in entry.items() if v is not None}
        data.append(entry)
        self._save_data(data)

    def delete_aeroplane(self, identifier: str) -> bool:
        data = self._load_data()
        initial_len = len(data)
        data = [x for x in data if x.get("icao24") != identifier and x.get("callsign") != identifier]
        if len(data) < initial_len:
            self._save_data(data)
            return True
        return False

    def get_all(self) -> list:
        raw = self._load_data()
        return [Aeroplane(**x) for x in raw]

    def filter_by_country(self, country: str) -> list:
        all_planes = self.get_all()
        country_lower = country.lower()
        return [p for p in all_planes if p.origin_country.lower() == country_lower]

    def clear(self) -> None:
        self.filepath.write_text("[]", encoding="utf-8")
