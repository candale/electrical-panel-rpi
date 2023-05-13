import pytest

import config
from config import load_lights


def test_load_lights_ok():
    lights = load_lights()
    assert len(lights) > 0


def test_bad_config_raises(monkeypatch):
    monkeypatch.setattr(config, 'configuration', {'lights': [{'wrong_key': 10}]})
    with pytest.raises(TypeError, match='Bad light config.*'):
        load_lights()
