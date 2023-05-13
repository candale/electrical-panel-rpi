import pytest
from collections import defaultdict

from in_out import core
from lights import Light


class IOState:

    def __init__(self):
        self._state = {}

    def __call__(self, *args, **kwargs):
        return self

    def set(self, number, state):
        self._state[number] = state

    def set_input_state(self, number, state):
        self._state[number + 1] = state

    def mock_readCh(self, stack, number):
        return self._state.get(number, False)

    def get(self, number):
        if number not in self._state:
            self._state[number] = False

        return self._state[number]

    def reset(self):
        self._state = {}


relay_state_store = IOState()
input_state_store = IOState()


@pytest.fixture(autouse=True)
def mock_read_ch(mocker):
    mocker.patch('in_out.core.readCh', side_effect=input_state_store.mock_readCh)


@pytest.fixture(autouse=True)
def mock_sm16relind(monkeypatch):
    monkeypatch.setattr(core, 'SM16relind', relay_state_store)


@pytest.fixture(autouse=True)
def reset_state_stores():
    relay_state_store.reset()
    input_state_store.reset()


@pytest.fixture
def relay_state():
    return relay_state_store


@pytest.fixture
def input_state():
    return input_state_store


@pytest.fixture
def light_factory():
    def make_light(**kwargs):
        light = Light(
            id=kwargs.get('id', 'kitchen_light'),
            verbose_name=kwargs.get('verbose_name', 'Kitchen light'),
            relay_no=kwargs.get('relay_no', 31),
            input_no=kwargs.get('input_no'),
            indirect=kwargs.get('indirect', False)
        )
        return light

    return make_light
