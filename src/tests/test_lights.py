import pytest
from in_out.core import read_relay, write_relay
from lights import Light, toggle_light, turn_on, turn_off


class TestDirectLight:

    def test_toggle_without_input_sets_relay_to_on(self, light_factory, relay_state):
        light = light_factory(indirect=False, relay_no=1, input_no=None)

        assert toggle_light(light) is True

        assert read_relay(light.relay_no) is True


    def test_turn_on_with_no_input_no_turns_on(self, light_factory):
        light = light_factory(indirect=False, relay_no=1, input_no=None)

        assert turn_on(light) is True
        assert read_relay(light.relay_no) is True


    def test_turn_on_with_input_no_turns_on(self, light_factory, input_state):
        light = light_factory(indirect=False, relay_no=1, input_no=1)

        input_state.set_input_state(light.input_no, True)
        assert turn_on(light) is True


    def test_turn_on_already_turned_on_does_not_write_relay(self, light_factory, input_state, mocker):
        light = light_factory(indirect=False, relay_no=1, input_no=1)

        input_state.set_input_state(light.input_no, True)
        write_relay_mock = mocker.patch('lights.write_relay')
        turn_on(light)

        write_relay_mock.assert_not_called()

    def test_turn_on_already_turned_on_no_input_no_does_not_write_relay(self, light_factory, mocker):
        light = light_factory(indirect=False, relay_no=1, input_no=None)

        write_relay(light.relay_no, True)
        write_relay_mock = mocker.patch('lights.write_relay')
        assert turn_on(light) is True
        write_relay_mock.assert_not_called()

    def test_turn_off_no_input_no_turns_off(self, light_factory):
        light = light_factory(indirect=False, relay_no=1, input_no=None)

        write_relay(light.relay_no, True)

        assert turn_off(light) is False

    def test_turn_off_with_input_no_turns_off(self, light_factory, input_state, mocker):
        light = light_factory(indirect=False, relay_no=1, input_no=1)

        input_state.set_input_state(light.input_no, False)
        assert turn_off(light) is False

    def test_turn_off_with_input_already_turned_off_does_not_write_relay(self, light_factory, input_state, mocker):
        light = light_factory(indirect=False, relay_no=1, input_no=1)

        input_state.set_input_state(light.input_no, False)
        write_relay_mock = mocker.patch('lights.write_relay')
        turn_off(light)

        write_relay_mock.assert_not_called()


class TestIndirectLight:

    def test_toggle_sets_on_then_off(self, light_factory, relay_state, mocker):
        light = light_factory(indirect=True, relay_no=1, input_no=2)

        mocked_write_relay = mocker.patch('lights.write_relay')
        toggle_light(light)

        mocked_write_relay.assert_has_calls([
            mocker.call(light.relay_no, True),
            mocker.call(light.relay_no, False)
        ])

    def test_turn_on_sets_relay_on_then_off(self, light_factory, mocker):
        light = light_factory(indirect=True, relay_no=1, input_no=1)

        mocked_write_relay = mocker.patch('lights.write_relay')
        turn_on(light)

        mocked_write_relay.assert_has_calls([
            mocker.call(light.relay_no, True),
            mocker.call(light.relay_no, False)
        ])

    def test_turn_on_already_turned_on_does_not_write_relay(self, light_factory, input_state, mocker):
        light = light_factory(indirect=True, relay_no=1, input_no=1)

        input_state.set_input_state(light.input_no, True)
        write_relay_mock = mocker.patch('lights.write_relay')
        turn_on(light)

        write_relay_mock.assert_not_called()


    def test_turn_off_sets_relay_on_then_off(self, light_factory, mocker,input_state):
        light = light_factory(indirect=True, relay_no=1, input_no=1)

        mocked_write_relay = mocker.patch('lights.write_relay')
        input_state.set_input_state(light.input_no, True)
        turn_off(light)

        mocked_write_relay.assert_has_calls([
            mocker.call(light.relay_no, True),
            mocker.call(light.relay_no, False)
        ])

    def test_turn_off_already_turned_off_does_not_write_relay(self, light_factory, input_state, mocker):
        light = light_factory(indirect=True, relay_no=1, input_no=1)

        input_state.set_input_state(light.input_no, False)
        write_relay_mock = mocker.patch('lights.write_relay')
        turn_off(light)

        write_relay_mock.assert_not_called()
