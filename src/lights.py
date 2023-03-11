from dataclasses import dataclass

from core import set_relay, read_input, toggle_relay


@dataclass
class Light:
    name: str
    relay_no: int
    input_no: int


def toggle_light(light: Light):
    toggle_relay(light.relay_no)
    return read_input(light.input_no)


def turn_on(light: Light):
    set_relay(light.relay_no, True)
    return read_input(light.input_no)


def turn_off(light: Light):
    set_relay(light.relay_no, False)
    return read_input(light.input_no)
