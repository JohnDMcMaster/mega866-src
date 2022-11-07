from gpio_controller import GpioController, all_earth_pins
from time import sleep
import sys

# NOTE: pin 45 needs to be conencted to ground manually using a jumper wire or the like.

# We assume one attached tl866 and we call it the "earth" controller
c = GpioController(
    earth_serial_device="/dev/serial/by-id/usb-ProgHQ_Open-TL866_Programmer_92DD659470E765C58847A4DA-if00"
)
c.init()


def pin(x):
    return 1 << (x - 1)


def pins(*pin_list):
    res = 0
    for p in pin_list:
        res |= pin(p)
    return res


def get_address_pins(input_pins):
    addr = 0
    for k, v in address_pins.items():
        if input_pins & (1 << (k - 1)):
            addr |= 1 << v
    return addr


def get_data_pins(input_pins):
    addr = 0
    for k, v in data_pins.items():
        if input_pins & (1 << (k - 1)):
            addr |= 1 << v
    return addr


def get_rw_pin(input_pins):
    if (input_pins & pin(RW_PIN)) > 0:
        return 1
    else:
        return 0


tristate_pins = all_earth_pins.copy()

# The letter 'B' at the end of a pin name means "bar", i.e., negated, active low

CLOCK_PIN = 59
RW_PIN = 65
RESET_PIN = 49

# Control pins
tristate_pins.remove(
    3
)  # IRQB: Interrupt request bar. Keep high to not trigger an interrupt.
tristate_pins.remove(
    7
)  # NMIB: Non-maskable interrupt bar. Keep high to not trigger an interrupt.
tristate_pins.remove(49)  # RESB: Reset bar. Keep high to not reset the CPU.
tristate_pins.remove(
    55
)  # RDY:  Ready. Keep to high to allow to CPU to operate normally.
tristate_pins.remove(
    57
)  # SOB:  Set overflow bar. Datasheet says it's not recommended to do anything with this pin other than tie it high.
tristate_pins.remove(
    59
)  # PHI2: Clock Input. The WDC W65C02S is a fully static design, so we can pulse the clock as slowly as we wish. May go up to 17MHz.
tristate_pins.remove(
    61
)  # BE:   Bus enable. Keep high to allow the CPU to put anything on the data and address bus.

# Data pins
data_pins = {11: 0, 13: 1, 15: 2, 17: 3, 19: 4, 21: 5, 77: 6, 79: 7}

for key in data_pins.keys():
    tristate_pins.remove(key)

# Address pins
address_pins = {
    69: 0,
    71: 1,
    73: 2,
    75: 3,
    23: 4,
    25: 5,
    27: 6,
    31: 7,
    35: 8,
    39: 9,
    43: 10,
    47: 11,
    41: 12,
    37: 13,
    33: 14,
    29: 15,
}

c.init()
c.io_tri(pins(*tristate_pins))
c.io_w(0)  # This should reset the 6502

always_high_pins = pins(3, 7, 49, 55, 57, 61)

# Always put 0xea on data bus, this is the no-op instruction
noop_instruction = pins(79, 77, 21, 17, 13)

c.io_w(always_high_pins | noop_instruction)

c.vdd_volt(1)  # 3.5V
c.vdd_pins(pins(67))  # VDD
c.vdd_en()

while True:
    input_pins = c.io_r()
    address = get_address_pins(input_pins)
    data = get_data_pins(input_pins)
    rw = get_rw_pin(input_pins)
    print(f"{address:#018x} {data:#010x} {'r' if rw == 1 else 'w'}")
    try:
        x = input("> ")
        if x == "q" or x == "quit":
            sys.exit(0)
    except EOFError:
        sys.exit(0)

    c.io_w(always_high_pins | noop_instruction | pin(CLOCK_PIN))
    sleep(0.001)
    c.io_w(always_high_pins | noop_instruction)
