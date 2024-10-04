import yaml

from lights import Light


configuration = {
    "lights": [
        {
            "id": "pantry_light",
            "verbose_name": "Pantry Light",
            "relay_no":  8,
            # panel analog: 18
            "input_no": 4,
            "indirect": True
        },
        {
            "id": "kitchen_led",
            "verbose_name": "Litchen Led",
            "relay_no":  9,
            # panel analog: 17
            "input_no": None,
            "indirect": True
        },
        {
            "id": "kitchen_light",
            "verbose_name": "Kitchen Light",
            "relay_no": 10,
            # panel analog: 16
            "input_no": 3,
            "indirect": True
        },
        {
            "id": "stairs_light",
            "verbose_name": "Stairs Light",
            "relay_no": 11,
            # panel analog: 14
            "input_no": 23,
            "indirect": True
        },
        {
            "id": "living_square_light",
            "verbose_name": "Living Square Light",
            "relay_no": 12,
            # panel analog: 13
            "input_no": 22,
            "indirect": True
        },
        {
            "id": "living_center_light",
            "verbose_name": "Living Center Light",
            "relay_no": 13,
            # panel analog: 12
            "input_no": 21,
            "indirect": True
        },
        {
            "id": "terrace_exit_light",
            "verbose_name": "Terrace Exit Light",
            "relay_no": 14,
            # panel analog: 11
            "input_no": 20,
            "indirect": True
        },
        {
            "id": "exterior_yard_light",
            "verbose_name": "Exterior Yard Light",
            "relay_no": 15,
            # panel analog: 21
            "input_no": 19,
            "indirect": True
        },
        {
            "id": "exterior_road_light",
            "verbose_name": "Exterior Road Light",
            "relay_no": 24,
            # panel analog: 20
            "input_no": 18,
            "indirect": True
        },
        {
            "id": "hallway_entrance_light",
            "verbose_name": "Hallway Entrance Light",
            "relay_no": 25,
            # panel analog: 19
            "input_no": 17,
            "indirect": True
        },
        {
            "id": "dinning_light",
            "verbose_name": "Dinning Light",
            "relay_no": 26,
            # panel analog: 10
            "input_no": 16,
            "indirect": True
        },
        {
            "id": "dinning_way_light",
            "verbose_name": "Dinning Way Light",
            "relay_no": 27,
            # panel analog: 9
            "input_no": 24,
            "indirect": True
        },
        {
            "id": "main_way_light",
            "verbose_name": "Main Way Light",
            "relay_no": 28,
            # panel analog: 8
            "input_no": 25,
            "indirect": True
        },
        {
            "id": "bedroom_way_light",
            "verbose_name": "Bedroom Way Light",
            "relay_no": 29,
            # panel analog: 7
            "input_no": 26,
            "indirect": True
        },
        {
            "id": "dressing_light",
            "verbose_name": "Dressing Light",
            "relay_no": 30,
            # panel analog: 5
            "input_no": 27,
            "indirect": True
        },
        {
            "id": "bathroom_shower_light",
            "verbose_name": "Bathroom Shower Light",
            "relay_no": 31,
            # panel analog: 4
            "input_no": 28,
            "indirect": True
        },
        {
            "id": "tub_shower_light",
            "verbose_name": "Bathroom Tub Light",
            "relay_no": 16,
            # panel analog: 3
            "input_no": 31,
            "indirect": True
        },
        {
            "id": "bedroom_small_light",
            "verbose_name": "Bedroom Small Light",
            "relay_no": 17,
            # panel analog: 2
            "input_no": 30,
            "indirect": True
        },
        {
            "id": "bedroom_master_light",
            "verbose_name": "Bedroom Master Light",
            "relay_no": 18,
            # panel analog: 1
            "input_no": 29,
            "indirect": True
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
