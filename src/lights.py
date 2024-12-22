import time
from dataclasses import dataclass

from in_out.core import (
    write_relay,
    read_input,
    toggle_relay,
    read_relay,
    read_all_inputs,
)


@dataclass
class Light:
    id: str
    verbose_name: str
    relay_no: int
    # when input_no is None, we run in "optimistic" mode, meaning that we assume
    # that the state of the light is actually what we set it to be
    input_no: int | None
    # This means that we don't control the light directly but through a latching
    # relay
    indirect: bool


def rock_indirect(light: Light):
    """Rock the relay to set the state for the latching relay"""
    write_relay(light.relay_no, True, lazy=True)
    time.sleep(0.2)
    write_relay(light.relay_no, False, lazy=True)


def get_light_state(light: Light):
    if light.indirect and light.input_no is None:
        raise ValueError("Cannot know if an indirect light is ON if no state pin")

    current_state = None
    if light.input_no is not None:
        current_state = read_input(light.input_no)
    elif light.indirect is False:
        current_state = read_relay(light.relay_no)

    return current_state


def get_many_lights_state(lights: list[Light]):
    states = {}
    all_inputs = read_all_inputs()
    for light in lights:
        if light.indirect and light.input_no is None:
            raise ValueError("Cannot know if an indirect light is ON if no state pin")

        states[light.input_no] = all_inputs[light.input_no]

    return states


def toggle_light(light: Light):
    """
    There's two cases:
    1. We get an input pin as well, where we can check the state of the light
    after it has been toggled.
    2. We don't have an input pin so we take the "optimistic" case, considerig
    that whatever the state of the relay is, that's the state of the light
    """
    new_state = None
    if light.indirect:
        rock_indirect(light)
    else:
        new_state = toggle_relay(light.relay_no)

    if light.input_no is not None:
        new_state = read_input(light.input_no)

    return new_state


def turn_on(light: Light):
    if light.indirect and light.input_no is None:
        raise ValueError("Cannot know if an indirect light is ON if no state pin")

    current_state = get_light_state(light)

    new_state = None
    if current_state is False:
        if light.indirect:
            rock_indirect(light)
        else:
            new_state = write_relay(light.relay_no, True)
    else:
        new_state = current_state

    if new_state is None:
        time.sleep(0.075)
        new_state = get_light_state(light)

    return new_state


def turn_off(light: Light):
    if light.indirect and light.input_no is None:
        raise ValueError("Cannot know if an indirect light is ON if no state pin")

    current_state = get_light_state(light)

    new_state = None
    if current_state is True:
        if light.indirect:
            rock_indirect(light)
        else:
            new_state = write_relay(light.relay_no, False)
    else:
        new_state = current_state

    if new_state is None:
        new_state = get_light_state(light)

    return new_state
