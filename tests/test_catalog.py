from datetime import date

import pytest

from transport_routes.errors import DuplicateId, NotFoundObject, WrongRoute
from transport_routes.models import Catalog, Route


def make_route(route_id="002", name="Вокзал", category="автобус"):
    return Route(route_id, name, category, date(2020, 5, 1), "Центр", "Парк")


def test_valid_route():

    route = make_route()

    assert route.id == "002"
    assert route.date == date(2020, 5, 1)


def test_invalid_route():

    with pytest.raises(WrongRoute):
        make_route(route_id=2)


def test_add_get_remove():

    catalog = Catalog()
    route = make_route()
    catalog.add(route)

    assert catalog.get(route.id) == route
    assert route.id in catalog
    assert len(catalog) == 1

    catalog.remove(route.id)

    assert route.id not in catalog
    assert len(catalog) == 0
    
    with pytest.raises(NotFoundObject):
        catalog.remove(route.id)


def test_duplicate_id():

    catalog = Catalog()
    route = make_route()
    catalog.add(route)


    with pytest.raises(DuplicateId):
        catalog.add(make_route(name="Другой маршрут"))

    assert catalog.get(route.id) == route


def test_search():
    catalog = Catalog()
    bus = make_route()
    catalog.add(bus)
    catalog.add(make_route("001", "Музей", "трамвай"))

    found = catalog.find_by_category("автобус")

    assert found == [bus]

    found.clear()

    assert catalog.find_by_name("ВОКЗАЛ") == [bus]

    assert len(catalog) == 2


def test_iteration_order():

    catalog = Catalog()
    first = make_route("002")
    second = make_route("001")


    catalog.add(first)
    catalog.add(second)


    assert list(catalog) == [first, second]
