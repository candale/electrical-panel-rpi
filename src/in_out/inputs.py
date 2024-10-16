DEVICE_ADDRESS = 0x20  # 7 bit address (will be left shifted to add the read write bit)
INPUTS16_INPORT_REG_ADD = 0
pinMask = [0x8000, 0x4000, 0x2000, 0x1000, 0x0800, 0x0400, 0x0200, 0x0100, 0x80, 0x40, 0x20, 0x10, 0x08, 0x04, 0x02,
           0x01]


def readCh(bus, stack, channel):
    if stack < 0 or stack > 7:
        raise ValueError('Invalid stack level')
    stack = 0x07 ^ stack
    if channel < 1 or channel > 16:
        raise ValueError('Invalid channel')
    hw_add = DEVICE_ADDRESS + stack
    val = bus.read_word_data(hw_add, INPUTS16_INPORT_REG_ADD)

    if val & pinMask[channel - 1] == 0:
        return 1
    return 0


def readAll(bus, stack):
    if stack < 0 or stack > 7:
        raise ValueError('Invalid stack level')
    stack = 0x07 ^ stack
    hw_add = DEVICE_ADDRESS + stack
    val = bus.read_word_data(hw_add, INPUTS16_INPORT_REG_ADD)

    ret = 0
    for i in range(16):
        if val & pinMask[i] == 0:
            ret += 1 << i
    return ret


def read_all(bus, stack) -> list:
    if stack < 0 or stack > 7:
        raise ValueError('Invalid stack level')
    stack = 0x07 ^ stack
    hw_add = DEVICE_ADDRESS + stack
    val = bus.read_word_data(hw_add, INPUTS16_INPORT_REG_ADD)

    ret = [] 
    for i in range(16):
        ret.append(val & pinMask[i] == 0)
    return ret

