from dataclasses import asdict
from datetime import date

import pytest

from transport_routes.errors import DamagedFile, UnsupportedFormatVersion, WrongRoute
from transport_routes.load_to_json import dict_to_json
from transport_routes.models import Catalog, Route
from transport_routes.read_json import add_to_promo_Catalog, json_to_list_of_dicts, overflow


def test_json_round_trip(tmp_path):

    path = tmp_path / "routes.json"
    source = Catalog()
    route = Route("002", "Вокзал", "автобус", date(2020, 5, 1), "Центр", "Парк")
    source.add(route)

    dict_to_json([asdict(item) for item in source], path)

    restored = Catalog()

    overflow(restored, add_to_promo_Catalog(json_to_list_of_dicts(path)))
    
    assert list(restored) == list(source)


def test_damaged_json(tmp_path):

    path = tmp_path / "routes.json"

    path.write_text("{", encoding="utf-8")

    with pytest.raises(DamagedFile):
        json_to_list_of_dicts(path)


def test_unknown_version(tmp_path):

    path = tmp_path / "routes.json"

    path.write_text('{"format_version": 2, "items": []}', encoding="utf-8")

    with pytest.raises(UnsupportedFormatVersion):
        json_to_list_of_dicts(path)


def test_failed_load_keeps_catalog(tmp_path):

    path = tmp_path / "routes.json"

    catalog = Catalog()
    original = Route("001", "Вокзал", "автобус", date(2020, 5, 1), "Центр", "Парк")

    catalog.add(original)

    first = {"id": "002", "name": "Музей", "category": "трамвай",
             "date": "01.05.2020", "origin": "Парк", "destination": "Музей"}
    
    second = dict(first, id="003", date="31.02.2020")

    dict_to_json([first, second], path)

    with pytest.raises(WrongRoute):
        
        records = json_to_list_of_dicts(path)
        overflow(catalog, add_to_promo_Catalog(records))

    assert list(catalog) == [original]
