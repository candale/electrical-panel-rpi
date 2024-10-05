import time

import lib16inpind
import SM16relind

from .inputs import readCh, readAll


def get_stack(number):
    relay_stack = SM16relind(number)
    return relay_stack


def get_stack_and_relay(number):
    """
    This assumes that the relay boards are on even levels in the stack
    """
    stack = (number // 16 ) * 2
    relay_stack = SM16relind.SM16relind(stack)
    relay = (number if number < 16 else number - 16) + 1
    return relay_stack, relay

def write_relay(number, state):
    relay_stack, relay = get_stack_and_relay(number)
    relay_stack.set(relay, state)

    return relay_stack.get(relay) == 1


def read_relay(number):
    relay_stack, relay = get_stack_and_relay(number)
    return relay_stack.get(relay) == 1


def rock_relay(number):
    relay_stack, relay = get_stack_and_relay(number)
    value = relay_stack.get(relay)
    relay_stack.set(relay, not value)
    time.sleep(0.3)
    relay_stack.set(relay, value)

    return relay_stack.get(relay) == 1


def toggle_relay(number):
    relay_stack, relay = get_stack_and_relay(number)
    value = relay_stack.get(relay)
    relay_stack.set(relay, not value)

    return relay_stack.get(relay) == 1


def clear_relays():
    for i in range(32):
        write_relay(i, False)


def get_stack_and_input(number):
    """
    This assumes that the relay boards are on odd levels in the stack
    """
    stack = (number // 16 ) * 2 + 1
    input_ch = (number if number < 16 else number - 16) + 1
    return stack, input_ch


def read_input(number):
    stack, input_ch = get_stack_and_input(number)
    state = lib16inpind.readCh(stack, input_ch) == 1
    return state


def read_all_inputs():
    """
    This assumes that we have only two boards with inputs, on level 1 and 3
    """
    first_stack = readAll(1)
    second_stack = readAll(3)

    return first_stack + second_stack
