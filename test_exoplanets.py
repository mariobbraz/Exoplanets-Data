import csv
import json
import pathlib

from exoplanets import check_duplicates
from exoplanets import clean_csv_data
from exoplanets import sort_data
from exoplanets import write_json


def test_check_duplicates():
    reader = [
        {"pl_name": "Earth"},
        {"pl_name": "Mars"},
        {"pl_name": "Venus"},
        {"pl_name": "Saturn"},
        {"pl_name": "Mercury"},
        {"pl_name": "Mars"},  # Duplicate
        {"pl_name": "Earth"},  # Duplicate
    ]
    result = check_duplicates(reader)

    expected_result = [
        {"pl_name": "Earth"},
        {"pl_name": "Mars"},
        {"pl_name": "Venus"},
        {"pl_name": "Saturn"},
        {"pl_name": "Mercury"},
    ]
    assert result == expected_result


def test_write_json(tmp_path):
    csv_file = tmp_path / "sample.csv"
    json_file = tmp_path / "output.json"

    csv_file.write_text(
        "name,age,city\n"
        "Alice,30,New York\n"
        "Bob,25,Los Angeles\n"
    )

    with csv_file.open() as f:
        reader = csv.DictReader(f)
        write_json(reader, json_file)

    data = json.loads(json_file.read_text())

    expected = [
        {"name": "Alice", "age": "30", "city": "New York"},
        {"name": "Bob", "age": "25", "city": "Los Angeles"},
    ]

    assert sorted(data, key=lambda x: x["name"]) == \
        sorted(expected, key=lambda x: x["name"])


def test_sort_data(tmp_path, monkeypatch):
    data = [
        {"pl_name": "B", "pl_rade": "0.40"},
        {"pl_name": "A", "pl_rade": "0.39"},
        {"pl_name": "C", "pl_rade": "0.50"},
    ]

    data_dir = tmp_path / "data"
    data_dir.mkdir()

    json_file = data_dir / "key_exoplanets.json"
    json_file.write_text(json.dumps(data), encoding="utf-8")

    monkeypatch.setattr("exoplanets.DATA_DIR", data_dir)

    result = sort_data(lambda x: float(x["pl_rade"]))

    assert [row["pl_name"] for row in result] == ["A", "B", "C"]
