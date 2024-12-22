import time
from threading import Lock, Thread
from copy import copy

from loguru import logger

from .relay import SM16relind
from .inputs import read_all, readCh, readAll
from .i2c import i2c_bus


class _LazyRelayStateManager:

    def __init__(self, write_every_ms=180):
        self.write_every_ms = write_every_ms

        self._relay_states: list[bool] = []
        self._last_written_states: list[bool] = list
        self._states_lock = Lock()
        self._initialized = False

        self._writer_thread = Thread(target=self._do_writes)

    def _initialize(self):
        self._relay_states = read_all_relays()
        self._last_written_states = copy(self._relay_states)
        self._writer_thread.start()
        self._initialized = True

    def set(self, relay_no, state):
        with self._states_lock:
            if self._initialized is False:
                self._initialize()

            logger.debug(f"Lazy setting {relay_no} to {state}")
            self._relay_states[relay_no] = state

    def get(self, relay_no):
        return self._relay_states[relay_no]

    def _do_writes(self):
        logger.debug("Writer thread started ...")
        while True:
            do_write = False
            with self._states_lock:
                if self._relay_states != self._last_written_states:
                    self._last_written_states = copy(self._relay_states)
                    do_write = True

            if do_write:
                logger.debug("Writing lazy states")
                write_all_relays(self._last_written_states)

            time.sleep(self.write_every_ms / 1000)


lazy_relay_state_manager = _LazyRelayStateManager()


def get_stack(number):
    relay_stack = SM16relind(number)
    return relay_stack


def get_stack_and_relay(number):
    """
    This assumes that the relay boards are on even levels in the stack
    """
    stack = (number // 16) * 2
    with i2c_bus() as bus:
        relay_stack = SM16relind(bus, stack)
    relay = (number if number < 16 else number - 16) + 1
    return relay_stack, relay


def write_relay(number, state, lazy=False):
    """
    The `number` arg starts from 0
    If `lazy` set to true, the change accumulates over a set period of time and
    it is written at the end of the write interval

    We if not lazy, we return the state of the relay, otherwise None becasue we
    don't yet know if the state got written
    """
    final_state = None
    if lazy:
        lazy_relay_state_manager.set(number, state)
    else:
        relay_stack, relay = get_stack_and_relay(number)
        relay_stack.set(relay, state)

        final_state = relay_stack.get(relay) == 1

    return final_state


def read_relay(number, lazy=False):
    state = None
    if lazy:
        state = lazy_relay_state_manager.get(number)
    else:
        relay_stack, relay = get_stack_and_relay(number)
        state = relay_stack.get(relay) == 1

    return state


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
    stack = (number // 16) * 2 + 1
    input_ch = (number if number < 16 else number - 16) + 1
    return stack, input_ch


def read_input(number):
    stack, input_ch = get_stack_and_input(number)
    with i2c_bus() as bus:
        state = readCh(bus, stack, input_ch) == 1
    return state


def read_all_inputs() -> list[bool]:
    """
    This assumes that we have only two boards with inputs, on level 1 and 3
    """
    with i2c_bus() as bus:
        first_stack = read_all(bus, 1)
        second_stack = read_all(bus, 3)

    return first_stack + second_stack


def read_all_relays() -> list[bool]:
    """
    This assumes that we have only two boards with relays, on level 0 and 2
    """
    with i2c_bus() as bus:
        first_stack = SM16relind(bus, 0)
        second_stack = SM16relind(bus, 2)

        states = first_stack.get_all_as_list() + second_stack.get_all_as_list()

    return states


def write_all_relays(states: list[bool]):
    if len(states) != 32:
        raise ValueError("This works only with two relay stacks on level 0 and 2")

    with i2c_bus() as bus:
        first_stack = SM16relind(bus, 0)
        second_stack = SM16relind(bus, 2)

        first_stack.set_all_from_list(states[:16])
        second_stack.set_all_from_list(states[16:])
