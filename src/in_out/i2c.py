import smbus2
from contextlib import contextmanager
from threading import Lock
from typing import Iterator


_i2c_bus: smbus2.SMBus | None = None
_lock = Lock()


def configure(i2c_bus_no):
    global _i2c_bus
    
    if _i2c_bus is None:
        _i2c_bus = smbus2.SMBus(i2c_bus_no)


@contextmanager
def i2c_bus() -> Iterator[smbus2.SMBus]:
    if _i2c_bus is None:
        raise TypeError('I2C bus not initialized')

    with _lock:
        yield _i2c_bus

