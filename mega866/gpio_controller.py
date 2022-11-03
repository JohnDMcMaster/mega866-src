#!/usr/bin/env python3

from enum import Enum
from typing import Dict, Iterator, List, Optional
from otl866.bitbang import Bitbang # type: ignore

TL866_LOWEST_PIN_NUMBER: int = 1
TL866_HIGHEST_PIN_NUMBER: int = 40

MEGA866_HIGHEST_PIN_NUMBER: int = 160
MEGA866_LOWEST_PIN_NUMBER: int = 1

class Tl866Instance(Enum):
    WATER = 1 # J9
    EARTH = 2 # J3
    FIRE = 3 # J5
    WIND = 4 # J7

class Tl866Pin:
    def __init__(self, instance: Tl866Instance, pin_on_tl866_instance: int):
        self.instance = instance
        self.bitbanger = None
        if not pin_on_tl866_instance in range(TL866_LOWEST_PIN_NUMBER, TL866_HIGHEST_PIN_NUMBER + 1):
            raise Exception(f"pin number {pin_on_tl866_instance} out of range [{TL866_LOWEST_PIN_NUMBER}, {TL866_HIGHEST_PIN_NUMBER}]")
        else:
            self.pin = pin_on_tl866_instance

pin2Tl866_map: Dict[int, Tl866Pin] = {
    51: Tl866Pin(Tl866Instance.EARTH, 1),
    55: Tl866Pin(Tl866Instance.EARTH, 2),
    1: Tl866Pin(Tl866Instance.EARTH, 3),
    3: Tl866Pin(Tl866Instance.EARTH, 4),
    5: Tl866Pin(Tl866Instance.EARTH, 5),
    7: Tl866Pin(Tl866Instance.EARTH, 6),
    9: Tl866Pin(Tl866Instance.EARTH, 7),
    67: Tl866Pin(Tl866Instance.EARTH, 8),
    69: Tl866Pin(Tl866Instance.EARTH, 9),
    71: Tl866Pin(Tl866Instance.EARTH, 10),
    73: Tl866Pin(Tl866Instance.EARTH, 11),
    75: Tl866Pin(Tl866Instance.EARTH, 12),
    23: Tl866Pin(Tl866Instance.EARTH, 13),
    25: Tl866Pin(Tl866Instance.EARTH, 14),
    27: Tl866Pin(Tl866Instance.EARTH, 15),
    31: Tl866Pin(Tl866Instance.EARTH, 16),
    35: Tl866Pin(Tl866Instance.EARTH, 17),
    39: Tl866Pin(Tl866Instance.EARTH, 18),
    43: Tl866Pin(Tl866Instance.EARTH, 19),
    47: Tl866Pin(Tl866Instance.EARTH, 20),
    45: Tl866Pin(Tl866Instance.EARTH, 21),
    41: Tl866Pin(Tl866Instance.EARTH, 22),
    37: Tl866Pin(Tl866Instance.EARTH, 23),
    33: Tl866Pin(Tl866Instance.EARTH, 24),
    29: Tl866Pin(Tl866Instance.EARTH, 25),
    79: Tl866Pin(Tl866Instance.EARTH, 26),
    77: Tl866Pin(Tl866Instance.EARTH, 27),
    21: Tl866Pin(Tl866Instance.EARTH, 28),
    19: Tl866Pin(Tl866Instance.EARTH, 29),
    17: Tl866Pin(Tl866Instance.EARTH, 30),
    15: Tl866Pin(Tl866Instance.EARTH, 31),
    13: Tl866Pin(Tl866Instance.EARTH, 32),
    11: Tl866Pin(Tl866Instance.EARTH, 33),
    65: Tl866Pin(Tl866Instance.EARTH, 34),
    63: Tl866Pin(Tl866Instance.EARTH, 35),
    61: Tl866Pin(Tl866Instance.EARTH, 36),
    59: Tl866Pin(Tl866Instance.EARTH, 37),
    57: Tl866Pin(Tl866Instance.EARTH, 38),
    53: Tl866Pin(Tl866Instance.EARTH, 39),
    49: Tl866Pin(Tl866Instance.EARTH, 40),

    97: Tl866Pin(Tl866Instance.WIND, 1),
    101: Tl866Pin(Tl866Instance.WIND, 2),
    105: Tl866Pin(Tl866Instance.WIND, 3),
    109: Tl866Pin(Tl866Instance.WIND, 4),
    113: Tl866Pin(Tl866Instance.WIND, 5),
    117: Tl866Pin(Tl866Instance.WIND, 6),
    121: Tl866Pin(Tl866Instance.WIND, 7),
    125: Tl866Pin(Tl866Instance.WIND, 8),
    129: Tl866Pin(Tl866Instance.WIND, 9),
    133: Tl866Pin(Tl866Instance.WIND, 10),
    135: Tl866Pin(Tl866Instance.WIND, 11),
    137: Tl866Pin(Tl866Instance.WIND, 12),
    139: Tl866Pin(Tl866Instance.WIND, 13),
    87: Tl866Pin(Tl866Instance.WIND, 14),
    89: Tl866Pin(Tl866Instance.WIND, 15),
    91: Tl866Pin(Tl866Instance.WIND, 16),
    93: Tl866Pin(Tl866Instance.WIND, 17),
    95: Tl866Pin(Tl866Instance.WIND, 18),
    153: Tl866Pin(Tl866Instance.WIND, 19),
    157: Tl866Pin(Tl866Instance.WIND, 20),
    159: Tl866Pin(Tl866Instance.WIND, 21),
    155: Tl866Pin(Tl866Instance.WIND, 22),
    151: Tl866Pin(Tl866Instance.WIND, 23),
    149: Tl866Pin(Tl866Instance.WIND, 24),
    147: Tl866Pin(Tl866Instance.WIND, 25),
    145: Tl866Pin(Tl866Instance.WIND, 26),
    143: Tl866Pin(Tl866Instance.WIND, 27),
    141: Tl866Pin(Tl866Instance.WIND, 28),
    85: Tl866Pin(Tl866Instance.WIND, 29),
    83: Tl866Pin(Tl866Instance.WIND, 30),
    81: Tl866Pin(Tl866Instance.WIND, 31),
    131: Tl866Pin(Tl866Instance.WIND, 32),
    127: Tl866Pin(Tl866Instance.WIND, 33),
    123: Tl866Pin(Tl866Instance.WIND, 34),
    119: Tl866Pin(Tl866Instance.WIND, 35),
    115: Tl866Pin(Tl866Instance.WIND, 36),
    111: Tl866Pin(Tl866Instance.WIND, 37),
    107: Tl866Pin(Tl866Instance.WIND, 38),
    103: Tl866Pin(Tl866Instance.WIND, 39),
    99: Tl866Pin(Tl866Instance.WIND, 40),

    48: Tl866Pin(Tl866Instance.FIRE, 1),
    44: Tl866Pin(Tl866Instance.FIRE, 2),
    40: Tl866Pin(Tl866Instance.FIRE, 3),
    36: Tl866Pin(Tl866Instance.FIRE, 4),
    32: Tl866Pin(Tl866Instance.FIRE, 5),
    28: Tl866Pin(Tl866Instance.FIRE, 6),
    26: Tl866Pin(Tl866Instance.FIRE, 7),
    24: Tl866Pin(Tl866Instance.FIRE, 8),
    76: Tl866Pin(Tl866Instance.FIRE, 9),
    74: Tl866Pin(Tl866Instance.FIRE, 10),
    72: Tl866Pin(Tl866Instance.FIRE, 11),
    70: Tl866Pin(Tl866Instance.FIRE, 12),
    68: Tl866Pin(Tl866Instance.FIRE, 13),
    10: Tl866Pin(Tl866Instance.FIRE, 14),
    8: Tl866Pin(Tl866Instance.FIRE, 15),
    6: Tl866Pin(Tl866Instance.FIRE, 16),
    4: Tl866Pin(Tl866Instance.FIRE, 17),
    2: Tl866Pin(Tl866Instance.FIRE, 18),
    56: Tl866Pin(Tl866Instance.FIRE, 19),
    52: Tl866Pin(Tl866Instance.FIRE, 20),
    50: Tl866Pin(Tl866Instance.FIRE, 21),
    54: Tl866Pin(Tl866Instance.FIRE, 22),
    58: Tl866Pin(Tl866Instance.FIRE, 23),
    60: Tl866Pin(Tl866Instance.FIRE, 24),
    62: Tl866Pin(Tl866Instance.FIRE, 25),
    64: Tl866Pin(Tl866Instance.FIRE, 26),
    66: Tl866Pin(Tl866Instance.FIRE, 27),
    12: Tl866Pin(Tl866Instance.FIRE, 28),
    14: Tl866Pin(Tl866Instance.FIRE, 29),
    16: Tl866Pin(Tl866Instance.FIRE, 30),
    18: Tl866Pin(Tl866Instance.FIRE, 31),
    20: Tl866Pin(Tl866Instance.FIRE, 32),
    22: Tl866Pin(Tl866Instance.FIRE, 33),
    78: Tl866Pin(Tl866Instance.FIRE, 34),
    80: Tl866Pin(Tl866Instance.FIRE, 35),
    30: Tl866Pin(Tl866Instance.FIRE, 36),
    34: Tl866Pin(Tl866Instance.FIRE, 37),
    38: Tl866Pin(Tl866Instance.FIRE, 38),
    42: Tl866Pin(Tl866Instance.FIRE, 39),
    46: Tl866Pin(Tl866Instance.FIRE, 40),

    158: Tl866Pin(Tl866Instance.WATER, 1),
    154: Tl866Pin(Tl866Instance.WATER, 2),
    96: Tl866Pin(Tl866Instance.WATER, 3),
    94: Tl866Pin(Tl866Instance.WATER, 4),
    92: Tl866Pin(Tl866Instance.WATER, 5),
    90: Tl866Pin(Tl866Instance.WATER, 6),
    88: Tl866Pin(Tl866Instance.WATER, 7),
    140: Tl866Pin(Tl866Instance.WATER, 8),
    138: Tl866Pin(Tl866Instance.WATER, 9),
    136: Tl866Pin(Tl866Instance.WATER, 10),
    134: Tl866Pin(Tl866Instance.WATER, 11),
    130: Tl866Pin(Tl866Instance.WATER, 12),
    126: Tl866Pin(Tl866Instance.WATER, 13),
    122: Tl866Pin(Tl866Instance.WATER, 14),
    118: Tl866Pin(Tl866Instance.WATER, 15),
    114: Tl866Pin(Tl866Instance.WATER, 16),
    110: Tl866Pin(Tl866Instance.WATER, 17),
    106: Tl866Pin(Tl866Instance.WATER, 18),
    102: Tl866Pin(Tl866Instance.WATER, 19),
    98: Tl866Pin(Tl866Instance.WATER, 20),
    100: Tl866Pin(Tl866Instance.WATER, 21),
    104: Tl866Pin(Tl866Instance.WATER, 22),
    108: Tl866Pin(Tl866Instance.WATER, 23),
    112: Tl866Pin(Tl866Instance.WATER, 24),
    116: Tl866Pin(Tl866Instance.WATER, 25),
    120: Tl866Pin(Tl866Instance.WATER, 26),
    124: Tl866Pin(Tl866Instance.WATER, 27),
    128: Tl866Pin(Tl866Instance.WATER, 28),
    132: Tl866Pin(Tl866Instance.WATER, 29),
    82: Tl866Pin(Tl866Instance.WATER, 30),
    84: Tl866Pin(Tl866Instance.WATER, 31),
    86: Tl866Pin(Tl866Instance.WATER, 32),
    142: Tl866Pin(Tl866Instance.WATER, 33),
    144: Tl866Pin(Tl866Instance.WATER, 34),
    146: Tl866Pin(Tl866Instance.WATER, 35),
    148: Tl866Pin(Tl866Instance.WATER, 36),
    150: Tl866Pin(Tl866Instance.WATER, 37),
    152: Tl866Pin(Tl866Instance.WATER, 38),
    156: Tl866Pin(Tl866Instance.WATER, 39),
    160: Tl866Pin(Tl866Instance.WATER, 40),
}

class GpioController:
    def __init__(self, water_serial_device: Optional[str] = None, earth_serial_device: Optional[str] = None, fire_serial_device: Optional[str] = None, wind_serial_device: Optional[str] = None) -> None:
        self.bitbangers: List[Bitbang] = []
        def add_device(self, device: Optional[str], instance: Tl866Instance):
            if device is not None:
                bb = Bitbang(device=device)
                self.bitbangers.append(bb)
                for value in pin2Tl866_map.values():
                     if value.instance == instance:
                        value.bitbanger = bb

        add_device(self, water_serial_device, Tl866Instance.WATER)
        add_device(self, earth_serial_device, Tl866Instance.EARTH)
        add_device(self, fire_serial_device, Tl866Instance.FIRE)
        add_device(self, wind_serial_device, Tl866Instance.WIND)

    def __iter__(self) -> Iterator[Bitbang]:
        return iter(self.bitbangers)

    def _get_pins_per_controller(self, val: int) -> Dict[Bitbang, int]:
        pins_per_tl866 = {}
        for controller in self:
            pins_per_tl866[controller] = 0
        for i in range(0, MEGA866_HIGHEST_PIN_NUMBER):
            if val & (1 << i):
                if (i + 1) not in pin2Tl866_map:
                    raise Exception(f"Pin {i + 1} is not valid")
                elif pin2Tl866_map[i + 1].bitbanger is None:
                    raise Exception(f"device for pin {i + 1} not given")
                else:
                    pins_per_tl866[pin2Tl866_map[i + 1].bitbanger] |= (1 << pin2Tl866_map[i + 1].pin - 1)
        return pins_per_tl866

    def vdd_en(self, enable: bool = True) -> None:
        for controller in self:
            controller.vdd_en()

    def vdd_volt(self, val: int) -> None:
        for controller in self:
            controller.vdd_volt(val)

    def vdd_pins(self, val: int) -> None:
        for controller, val in self._get_pins_per_controller(val).items():
            controller.vdd_pins(val)

    def vpp_en(self, enable: bool = True) -> None:
        for controller in self:
            controller.vpp_en()

    def vpp_volt(self, val: int) -> None:
        for controller in self:
            controller.vpp_volt(val)

    def vpp_pins(self, val: int) -> None:
        for controller, val in self._get_pins_per_controller(val).items():
            controller.vpp_pins(val)

    def gnd_pins(self, val: int) -> None:
        for controller, val in self._get_pins_per_controller(val).items():
            controller.gnd_pins(val)

    def io_tri(self, val: int = int("ff" * 5 * 4, base=16)):
        for controller, val in self._get_pins_per_controller(val).items():
            controller.io_tri(val)

def main() -> None:
    '''
    This turns on 9.9v across pins 1 and 2 on a single controller
    controller = GpioController(earth_serial_device="/dev/serial/by-id/usb-ProgHQ_Open-TL866_Programmer_92DD659470E765C58847A4DA-if00")
    controller.vpp_pins((1 << 50))
    controller.vpp_volt(0)
    controller.vpp_en()
    controller.vdd_en()
    controller.gnd_pins((1 << 2))
    '''
    pass

if __name__ == '__main__':
    main()
