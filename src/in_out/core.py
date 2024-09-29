import time


from .relay import SM16relind
from .inputs import readCh


def get_stack(number):
    relay_stack = SM16relind(number)
    return relay_stack


def get_stack_and_relay(number):
    stack = (number // 16 ) * 2
    relay_stack = SM16relind(stack)
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
    stack = 1 if number < 16 else 3
    input_ch = (number if number < 16 else number - 16) + 1
    return stack, input_ch


def read_input(number):
    stack, input_ch = get_stack_and_input(number)
    return readCh(stack, input_ch) == 1
