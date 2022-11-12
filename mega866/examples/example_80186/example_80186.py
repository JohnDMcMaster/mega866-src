from gpio_controller import GpioController, all_pins
from time import sleep

# We are using the PGA132 adapter
# We are using the PGA68

def pin(x):
    return 1 << (x - 1)


def pins(*pin_list):
    res = 0
    for p in pin_list:
        res |= pin(p)
    return res

plccpin2socketpin = [
        33,
        31,
        35,
        37,
        39,
        41,
        43,
        45,
        47,
        48,
        46,
        44,
        42,
        40,
        38,
        36,
        34,
        32,
        30,
        28,
        26,
        24,
        22,
        20,
        18,
        16,
        14,
        68,
        12,
        10,
        66,
        8,
        64,
        6,
        62,
        4,
        60,
        2,
        58,
        56,
        54,
        52,
        50,
        49,
        51,
        53,
        55,
        57,
        1,
        59,
        3,
        61,
        5,
        63,
        7,
        65,
        9,
        11,
        67,
        13,
        15,
        17,
        19,
        21,
        23,
        25,
        27,
        29,
]

# A/D = address/data
# The address and data lines are multiplexed

address_data_pins = [
    34, # A/D  0
    38, # A/D  1
    42, # A/D  2
    46, # A/D  3
    45, # A/D  4
    41, # A/D  5
    37, # A/D  6
    31, # A/D  7
    36, # A/D  8
    40, # A/D  9
    44, # A/D 10
    48, # A/D 11
    43, # A/D 12
    39, # A/D 13
    35, # A/D 14
    33, # A/D 15
    29, # A   16
    27, # A   17
    25, # A   18
    23, # A   19
]

# Inputs
VCCs = [47, 50] # +5 Volts. Unfortunately, pin 47 cannot be set to VDD or VPP :(
VSSs = [13, 16] # Ground
RES = 20 # Reset, active low
X1  = 67 # Clock
TMR_IN_0 = 28 # Timer input, drive high to ignore
TMR_IN_1 = 26 # Timer input, drive high to ignore
DRQ_0 = 32 # DMA Request, pull low
DRQ_1 = 30 # DMA Request, pull low
NMI = 53 # Non-maskable interrupt, pull low
INT0 = 51 # Maskable interupt request, pull low
INT1 = 49 # Maskable interupt request, pull low
INT2 = 52 # Maskable interupt request, pull low
INT3 = 54 # Maskable interupt request, pull low
ARDY = 7 # Asynchronous ready, pull low
SRDY = 1 # Synchronous ready, pull high?
HOLD = 59 # Hold, pull low
PEREQ = 2 # processor extension request, pull low
ERROR = 60 # Signal numerics coprocessor errors, active low, pull high

# Output
DEN = 58 # Data Enable, low on each memory and I/O access
DT_R = 56 # Data transmit/receive, controls direction of data flow. Low = data read, high = data write
BHE = 21 # Bus high enable
ALE = 15 # Address latch enable
WR = 19 # Write strobe, low = data on bus to be written, high = queue status mode
RD = 17 # Read strobe, low = data on bus to be read, high = queue status mode
S0 = 61
S1 = 5
S2 = 63
LOCK = 57

tristate_pins = set(all_pins)

# These pins should always be driven
for p in [RES, X1, TMR_IN_0, TMR_IN_1, DRQ_0, DRQ_1, NMI, INT0, INT1, INT2, INT3, ARDY, SRDY, HOLD, PEREQ, ERROR]:
    tristate_pins.remove(p)

always_high_pins = [TMR_IN_0, TMR_IN_1, ERROR, SRDY]

def display_pins(read_pins):
    for p in [["DEN", DEN], ["RD", RD], ["WR", WR], ["S0", S0], ["S1", S1], ["S2", S2], ["LOCK", LOCK]]:
        name = p[0]
        bit = 1 if (pin(p[1]) & read_pins) > 0 else 0
        print(f"{name:<10}: {bit}")

def do_bus_cycles(controller):
    for _ in range(10):
        controller.io_w(pins(*always_high_pins))
        sleep(0.001)
        controller.io_w(pins(*always_high_pins) | pin(X1))
        sleep(0.001)
        display_pins(controller.io_r())


def main():
    controller = GpioController(earth_serial_device="/dev/serial/by-id/usb-ProgHQ_Open-TL866_Programmer_BB7DE095C3656D924B371EC8-if00", water_serial_device="/dev/serial/by-id/usb-ProgHQ_Open-TL866_Programmer_92DD659470E765C58847A4DA-if00", fire_serial_device="/dev/serial/by-id/usb-ProgHQ_Open-TL866_Programmer_000000000000000000000000-if00", wind_serial_device="/dev/serial/by-id/usb-ProgHQ_Open-TL866_Programmer_33144A91666856D18E6084EC-if00")

    controller.init()
    controller.io_tri(pins(*tristate_pins))
    controller.vdd_volt(3) # 5.1V
    controller.vdd_pins(pin(50))
    controller.gnd_pins(pins(*VSSs))
    controller.vdd_en()
    controller.io_w(pins(*always_high_pins))
    sleep(0.001)
    always_high_pins.append(RES)
    controller.io_w(pins(*always_high_pins))
    sleep(0.001)

    do_bus_cycles(controller)

def test():
    import pdb
    controller = GpioController(earth_serial_device="/dev/serial/by-id/usb-ProgHQ_Open-TL866_Programmer_BB7DE095C3656D924B371EC8-if00", water_serial_device="/dev/serial/by-id/usb-ProgHQ_Open-TL866_Programmer_92DD659470E765C58847A4DA-if00", fire_serial_device="/dev/serial/by-id/usb-ProgHQ_Open-TL866_Programmer_000000000000000000000000-if00", wind_serial_device="/dev/serial/by-id/usb-ProgHQ_Open-TL866_Programmer_33144A91666856D18E6084EC-if00")

    controller.init()
    controller.io_tri(0)

    pdb.set_trace()
    for i, p in enumerate(plccpin2socketpin):
        print(f"i: {i:2}, p: {p:3}")
        controller.io_w(pin(p))

if __name__ == "__main__":
    #main()
    test()
