from dataclasses import dataclass
from collections.abc import Iterator
from datetime import date


from .errors import DuplicateId, NotFoundObject, WrongRoute

@dataclass(frozen=True)
class Route():
    id: str
    name: str
    category: str
    date: date
    origin: str
    destination: str


    def __post_init__(self) -> None:

        if not isinstance(self.id, str):
            raise WrongRoute(f"Поле id {self.id} не соответствует формату!")

        for field_name in ("name", "category", "origin", "destination"):
            if not isinstance(getattr(self, field_name), str):
                raise WrongRoute(f"Поле {field_name} должно быть строкой")

        if type(self.date) is not date:
            raise WrongRoute(f"Неподдерживаемый формат поля date: {self.date}")

        if self.date > date.today():
            raise WrongRoute(f"Мы не обслуживаем клиентов, прибывших из будущего! Date from future {self.date}")

    

class Catalog:

    def __init__(self) -> None:
        self.__items = {}


    def add(self, item: Route) -> None:

        if item.id in self.__items.keys():
            raise DuplicateId(f"Дублирование id: {item.id}")

        self.__items[item.id] = {
            "name": item.name,
            "category": item.category,
            "date": item.date,
            "origin": item.origin,
            "destination": item.destination
        }
        

    def get(self, item_id: str) -> Route:

        if item_id not in self.__items.keys():
            raise NotFoundObject(f"Объект {item_id} не найден")


        return Route(item_id, **self.__items[item_id])
    
    def remove(self, item_id: str) -> None:

        if item_id not in self.__items.keys():
            raise NotFoundObject(f"Объект {item_id} не найден")

        del self.__items[item_id]

    def find_by_category(self, category: str) -> list[Route]:

        return [ Route(route[0], **route[1]) for route in self.__items.items() if route[1]["category"] == category] 


    def find_by_name(self, query: str) -> list[Route]:

        return [ Route(route[0], **route[1]) for route in self.__items.items() if route[1]["name"].lower() == query.lower()] 

        

    def __len__(self) -> int:
        return len(self.__items)

    def __iter__(self) -> Iterator:
        """Выдаёт маршруты в порядке добавления в каталог"""
        for item_id, item in self.__items.items():
            yield Route(item_id, **item)
        

    def __contains__(self, item_id: str):
        return item_id in self.__items


