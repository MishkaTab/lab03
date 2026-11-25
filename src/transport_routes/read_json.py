import json
from datetime import datetime

from .errors import DamagedFile, UnsupportedFormatVersion, WrongRoute, DuplicateId
from .models import Route, Catalog

def json_to_list_of_dicts(path:str) -> list[dict]:

    with open(path, encoding="utf-8") as f:

        try:
            routes = json.loads(f.read())
        except (json.JSONDecodeError, UnicodeDecodeError) as error:
            raise DamagedFile(f"Не удалось прочитать JSON из {path}") from error

        if not isinstance(routes, dict):
            raise DamagedFile(f"Пустой файл {path}")

        if "format_version" not in routes:
            raise DamagedFile(f"Отсутствует поле формата файла {path}")

        if routes["format_version"] != 1:
            raise UnsupportedFormatVersion(f"Неподдерживаемый формат файла: {routes["format_version"]}")

        items = routes.get("items")
        if not isinstance(items, list):
            raise DamagedFile("Поле items должно содержать список маршрутов")

        for item in items:
            if not isinstance(item, dict):
                raise DamagedFile(f"Запись {item} в items должна быть объектом")

    return items

def add_to_promo_Catalog(routes: list[dict]) -> Catalog:

    promo_catalog = Catalog()

    for el in routes:

        try:
            current_date = datetime.strptime(el["date"], "%d.%m.%Y").date()
        except (KeyError, TypeError, ValueError) as error:
            raise WrongRoute("Поле date должно содержать данные в формате ДД.ММ.ГГГГ") from error

        current_route = {**el, "date": current_date}
        
        try: 


            route = Route(**current_route)
        except TypeError as error:
            raise WrongRoute(f"Неверно переданные данные") from error

        promo_catalog.add(route)

    

    return promo_catalog


def overflow(original_catalog: Catalog, promo_catalog: Catalog) -> None:

    for route in promo_catalog.__iter__():
        try:
            original_catalog.add(route)
        except DuplicateId:
            continue





        











