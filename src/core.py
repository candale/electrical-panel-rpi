import time


from relay import SM16relind
from inputs import readCh


first_relay_stack = SM16relind(0)
second_relay_stack = SM16relind(2)


def get_stack_and_relay(number):
    stack = (number // 16 ) * 2
    relay_stack = SM16relind(stack)
    relay = (number if number < 16 else number - 16) + 1
    return relay_stack, relay

def set_relay(number, state):
    relay_stack, relay = get_stack_and_relay(number)
    relay_stack.set(relay, state)


def rock_relay(number):
    relay_stack, relay = get_stack_and_relay(number)
    value = relay_stack.get(relay)
    relay_stack.set(relay, not value)
    time.sleep(0.3)
    relay_stack.set(relay, value)


def toggle_relay(number):
    relay_stack, relay = get_stack_and_relay(number)
    value = relay_stack.get(relay)
    relay_stack.set(relay, not value)


def clear_relays():
    for i in range(32):
        set_relay(i, False)


def get_stack_and_input(number):
    stack = 1 if number < 16 else 3
    input_ch = (number if number < 16 else number - 16) + 1
    return stack, input_ch


def read_input(number):
    stack, input_ch = get_stack_and_input(number)
    return readCh(stack, input_ch)

