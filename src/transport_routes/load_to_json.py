import json
from datetime import date
from copy import deepcopy


def dict_to_json(items: list[dict], path: str) -> None:

    records = []

    for item in items:

        record = deepcopy(item)

        if isinstance(record["date"], date):
            record["date"] = record["date"].strftime("%d.%m.%Y")


        records.append(record)

    with open(path, "w", encoding="utf-8") as f:
        json.dump({"format_version": 1, "items": records}, f, indent=4)
