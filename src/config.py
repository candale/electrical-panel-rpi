import yaml

from lights import Light


configuration = {
    "lights": [
        {
            "id": "dinning",
            "verbose_name": "Dinning",
            "relay_no": 0,
            "input_no": 0,
            "indirect": False
        },
        {
            "id": "kitchen",
            "verbose_name": "Kitchen",
            "relay_no": 1,
            "input_no": 1,
            "indirect": False
        },
        {
            "id": "main_living",
            "verbose_name": "Main living",
            "relay_no": 2,
            "input_no": 2,
            "indirect": False
        },
        {
            "id": "living_square",
            "verbose_name": "Living square",
            "relay_no": 3,
            "input_no": 3,
            "indirect": False
        },
        {
            "id": "hallway",
            "verbose_name": "Hallway",
            "relay_no": 4,
            "input_no": 4,
            "indirect": False
        },
        {
            "id": "living_path_1",
            "verbose_name": "Living path 1",
            "relay_no": 5,
            "input_no": 5,
            "indirect": False
        },
        {
            "id": "living_path_2",
            "verbose_name": "Living path 2",
            "relay_no": 6,
            "input_no": 6,
            "indirect": False
        },
        {
            "id": "terace_exit",
            "verbose_name": "Terace exit",
            "relay_no": 7,
            "input_no": 7,
            "indirect": False
        }
    ]
}


def load_lights() -> list[Light]:
    lights = []
    for index, light_config in enumerate(configuration["lights"]):
        try:
            lights.append(Light(**light_config))
        except TypeError as e:
            raise TypeError(f'Bad light config at index {index}') from e

    return lights
