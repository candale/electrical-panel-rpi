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


def test_indirect_with_no_input_no_raises(monkeypatch):
    monkeypatch.setattr(
        config,
        'configuration',
        {
            'lights': [
                {
                    "id": "living_path_1",
                    "verbose_name": "Living path 1",
                    "relay_no": 5,
                    "input_no": None,
                    "indirect": True
                },
            ]
        }
    )

    with pytest.raises(ValueError, match='Cannot have an indirect light without input_no.*'):
        load_lights()
