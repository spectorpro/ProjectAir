from src.nominatim_api import NominatimApiClient
from src.opensky_api import OpenskyApiClient
from src.aeroplane import Aeroplane
from src.json_saver import JSONSaver


def user_interaction():
    nom = NominatimApiClient()
    sky = OpenskyApiClient()
    saver = JSONSaver("aeroplanes.json")

    country_name = input("Введите название страны: ").strip()
    if not country_name:
        print("Название страны не может быть пустым.")
        return

    try:
        south, west, north, east = nom.get_country_bbox(country_name)
    except Exception as e:
        print(f"Ошибка получения координат: {e}")
        return

    print(f"Координаты области: south={south}, west={west}, north={north}, east={east}")

    try:
        states = sky.get_aeroplanes_in_area(south, west, north, east)
    except Exception as e:
        print(f"Ошибка запроса к OpenSky: {e}")
        return

    aeroplanes = Aeroplane.cast_to_object_list(states)
    print(f"Найдено самолётов: {len(aeroplanes)}")

    # Сохраняем в JSON
    for a in aeroplanes:
        saver.add_aeroplane(a)

    # Топ N по высоте
    top_n_str = input("Введите количество самолётов для вывода в топ N по высоте: ").strip()
    try:
        top_n = int(top_n_str)
        if top_n <= 0:
            raise ValueError
    except ValueError:
        print("Некорректное значение N, используем 5.")
        top_n = 5

    sorted_by_alt = sorted(aeroplanes, key=lambda x: x.geo_altitude, reverse=True)
    top_alt = sorted_by_alt[:top_n]
    print("\nТоп самолётов по высоте:")
    for i, a in enumerate(top_alt, 1):
        print(f"{i}. Callsign: {a.callsign}, Country: {a.origin_country}, "
              f"Altitude: {a.geo_altitude:.1f} м, Velocity: {a.velocity:.1f} м/с")

    # Фильтрация по стране регистрации
    filter_countries = input("Введите названия стран для фильтрации по стране регистрации (через пробел): ").strip()
    if filter_countries:
        countries_list = [c.strip() for c in filter_countries.split()]
        filtered = [a for a in aeroplanes if a.origin_country in countries_list]
        print(f"\nОтфильтровано по странам: {countries_list}")
        print(f"Количество: {len(filtered)}")
        for i, a in enumerate(filtered, 1):
            print(f"{i}. Callsign: {a.callsign}, Country: {a.origin_country}, "
                  f"Altitude: {a.geo_altitude:.1f} м")

if __name__ == "__main__":
    user_interaction()
