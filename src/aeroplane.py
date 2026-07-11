from dataclasses import dataclass, field
from typing import Optional

@dataclass
class Aeroplane:
    callsign: str
    origin_country: str
    velocity: float  # м/с
    geo_altitude: float  # метры
    # дополнительные атрибуты
    icao24: Optional[str] = None
    longitude: Optional[float] = None
    latitude: Optional[float] = None

    def __post_init__(self):
        self._validate()

    def _validate(self):
        if not self.callsign or not isinstance(self.callsign, str):
            raise ValueError("Callsign должен быть непустой строкой.")
        if not self.origin_country or not isinstance(self.origin_country, str):
            raise ValueError("Origin country должен быть непустой строкой.")
        if self.velocity < 0:
            raise ValueError("Velocity не может быть отрицательным.")
        if self.geo_altitude < 0:
            raise ValueError("Geo altitude не может быть отрицательным.")

    # Сравнение по скорости
    def __lt__(self, other: "Aeroplane") -> bool:
        return self.velocity < other.velocity

    def __le__(self, other: "Aeroplane") -> bool:
        return self.velocity <= other.velocity

    def __gt__(self, other: "Aeroplane") -> bool:
        return self.velocity > other.velocity

    def __ge__(self, other: "Aeroplane") -> bool:
        return self.velocity >= other.velocity

    # Сравнение по высоте (отдельный метод, чтобы явно соответствовать заданию)
    @staticmethod
    def compare_by_altitude(a: "Aeroplane", b: "Aeroplane") -> int:
        """Возвращает -1, 0, 1 как в классических компараторах."""
        if a.geo_altitude < b.geo_altitude:
            return -1
        elif a.geo_altitude > b.geo_altitude:
            return 1
        return 0

    @classmethod
    def from_opensky_state(cls, state):
        """
        state — строка из states[i] от OpenSky:
        [0]=icao24, [1]=callsign, [2]=origin_country, [3]=time_position,
        [4]=last_contact, [5]=longitude, [6]=latitude, [7]=baro_altitude,
        [8]=on_ground, [9]=velocity, [10]=true_track, [11]=vertical_rate,
        [12]=sensors, [13]=geo_altitude, [14]=squawk, [15]=spi, [16]=position_source
        """
        icao24 = state[0]
        callsign = state[1]
        origin_country = state[2]
        velocity = float(state[9]) if state[9] is not None else 0.0
        geo_altitude = float(state[13]) if state[13] is not None else 0.0
        longitude = float(state[5]) if state[5] is not None else None
        latitude = float(state[6]) if state[6] is not None else None

        return cls(
            callsign=callsign,
            origin_country=origin_country,
            velocity=velocity,
            geo_altitude=geo_altitude,
            icao24=icao24,
            longitude=longitude,
            latitude=latitude,
        )

    @classmethod
    def cast_to_object_list(cls, states):
        """Преобразует список states от OpenSky в список объектов Aeroplane."""
        objects = []
        for s in states:
            try:
                obj = cls.from_opensky_state(s)
                objects.append(obj)
            except Exception:
                # Пропускаем некорректные строки, чтобы не ломать весь запрос
                continue
        return objects
