import pytest
from src.aeroplane import Aeroplane
from src.json_saver import JSONSaver
from pathlib import Path
import tempfile
import os

def test_aeroplane_validation_bad_velocity():
    with pytest.raises(ValueError):
        Aeroplane("TEST", "USA", -10, 1000)

def test_aeroplane_comparison_by_speed():
    a1 = Aeroplane("A1", "USA", 100, 5000)
    a2 = Aeroplane("A2", "USA", 200, 6000)
    assert a1 < a2
    assert a2 > a1

def test_aeroplane_compare_by_altitude():
    a1 = Aeroplane("A1", "USA", 100, 5000)
    a2 = Aeroplane("A2", "USA", 100, 7000)
    assert Aeroplane.compare_by_altitude(a1, a2) == -1
    assert Aeroplane.compare_by_altitude(a2, a1) == 1
    assert Aeroplane.compare_by_altitude(a1, Aeroplane("A3", "USA", 100, 5000)) == 0

def test_json_saver_add_and_get():
    tmp_path = Path(tempfile.mkdtemp()) / "test.json"
    saver = JSONSaver(str(tmp_path))
    a = Aeroplane("TEST123", "RU", 250.0, 11000.0, icao24="ABCD1234")
    saver.add_aeroplane(a)
    all_planes = saver.get_all()
    assert len(all_planes) == 1

def test_aeroplane_validation_bad_altitude():
    with pytest.raises(ValueError):
        Aeroplane("TEST", "USA", 100, -100)

def test_aeroplane_validation_empty_name():
    with pytest.raises(ValueError):
        Aeroplane("", "USA", 100, 1000)
