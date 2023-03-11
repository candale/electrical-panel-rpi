# Electrical pannel unitilies

Main boards: four stacks from Sequent Microsystem, 16 relay board and 16 input board.

## Overview

Very much work in progress.

The following things are defined so far:
- `core.py` contains the basic functions for I/O (`set_relay`, `read_input` etc)
- `lights.py` basically nothing, but should define what a basic light looks like
and offer functions for control
- `config.py` contains the lightning configuration

## Get started

Use the `run` script to get the things running:
```shell

# build the docker image
./run build

# run a shell in the image
./run shell

# start the MQTT broker
./run broker

# run, interactively, an mqtt client
# drops in a shell where you have var `client` for an mqtt client
./run script mqtt.py
```

## Notes

- Inspiration: https://github.com/thomasjsn/rpi-alarm
