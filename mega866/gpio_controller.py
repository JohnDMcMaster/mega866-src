#!/usr/bin/env python3

from enum import Enum
from typing import Dict, Iterator, List, Optional
from otl866.bitbang import Bitbang  # type: ignore

TL866_LOWEST_PIN_NUMBER: int = 1
TL866_HIGHEST_PIN_NUMBER: int = 40

MEGA866_HIGHEST_PIN_NUMBER: int = 160
MEGA866_LOWEST_PIN_NUMBER: int = 1


class Tl866Instance(Enum):
    WATER = 1  # J9
    EARTH = 2  # J3
    FIRE = 3  # J5
    WIND = 4  # J7


class Tl866Pin:
    def __init__(self, instance: Tl866Instance, pin_on_tl866_instance: int):
        self.instance = instance
        self.bitbanger = None
        if not pin_on_tl866_instance in range(
            TL866_LOWEST_PIN_NUMBER, TL866_HIGHEST_PIN_NUMBER + 1
        ):
            raise Exception(
                f"pin number {pin_on_tl866_instance} out of range [{TL866_LOWEST_PIN_NUMBER}, {TL866_HIGHEST_PIN_NUMBER}]"
            )
        else:
            self.pin = pin_on_tl866_instance


pin2Tl866_map: Dict[int, Tl866Pin] = {}
Tl866Pin2megaPin_map: Dict[Tl866Instance, List[int]] = {
    Tl866Instance.WATER: [0] * (TL866_HIGHEST_PIN_NUMBER + 1),
    Tl866Instance.EARTH: [0] * (TL866_HIGHEST_PIN_NUMBER + 1),
    Tl866Instance.FIRE: [0] * (TL866_HIGHEST_PIN_NUMBER + 1),
    Tl866Instance.WIND: [0] * (TL866_HIGHEST_PIN_NUMBER + 1),
}


def _add_mapping_entry(
    mega_pin: int, tl866_instance: Tl866Instance, tl866_pin: int
) -> None:
    if mega_pin in pin2Tl866_map:
        raise Exception("Pin already in map!")
    else:
        pin2Tl866_map[mega_pin] = Tl866Pin(tl866_instance, tl866_pin)
        Tl866Pin2megaPin_map[tl866_instance][tl866_pin] = mega_pin


_add_mapping_entry(51, Tl866Instance.EARTH, 1)
_add_mapping_entry(55, Tl866Instance.EARTH, 2)
_add_mapping_entry(1, Tl866Instance.EARTH, 3)
_add_mapping_entry(3, Tl866Instance.EARTH, 4)
_add_mapping_entry(5, Tl866Instance.EARTH, 5)
_add_mapping_entry(7, Tl866Instance.EARTH, 6)
_add_mapping_entry(9, Tl866Instance.EARTH, 7)
_add_mapping_entry(67, Tl866Instance.EARTH, 8)
_add_mapping_entry(69, Tl866Instance.EARTH, 9)
_add_mapping_entry(71, Tl866Instance.EARTH, 10)
_add_mapping_entry(73, Tl866Instance.EARTH, 11)
_add_mapping_entry(75, Tl866Instance.EARTH, 12)
_add_mapping_entry(23, Tl866Instance.EARTH, 13)
_add_mapping_entry(25, Tl866Instance.EARTH, 14)
_add_mapping_entry(27, Tl866Instance.EARTH, 15)
_add_mapping_entry(31, Tl866Instance.EARTH, 16)
_add_mapping_entry(35, Tl866Instance.EARTH, 17)
_add_mapping_entry(39, Tl866Instance.EARTH, 18)
_add_mapping_entry(43, Tl866Instance.EARTH, 19)
_add_mapping_entry(47, Tl866Instance.EARTH, 20)
_add_mapping_entry(45, Tl866Instance.EARTH, 21)
_add_mapping_entry(41, Tl866Instance.EARTH, 22)
_add_mapping_entry(37, Tl866Instance.EARTH, 23)
_add_mapping_entry(33, Tl866Instance.EARTH, 24)
_add_mapping_entry(29, Tl866Instance.EARTH, 25)
_add_mapping_entry(79, Tl866Instance.EARTH, 26)
_add_mapping_entry(77, Tl866Instance.EARTH, 27)
_add_mapping_entry(21, Tl866Instance.EARTH, 28)
_add_mapping_entry(19, Tl866Instance.EARTH, 29)
_add_mapping_entry(17, Tl866Instance.EARTH, 30)
_add_mapping_entry(15, Tl866Instance.EARTH, 31)
_add_mapping_entry(13, Tl866Instance.EARTH, 32)
_add_mapping_entry(11, Tl866Instance.EARTH, 33)
_add_mapping_entry(65, Tl866Instance.EARTH, 34)
_add_mapping_entry(63, Tl866Instance.EARTH, 35)
_add_mapping_entry(61, Tl866Instance.EARTH, 36)
_add_mapping_entry(59, Tl866Instance.EARTH, 37)
_add_mapping_entry(57, Tl866Instance.EARTH, 38)
_add_mapping_entry(53, Tl866Instance.EARTH, 39)
_add_mapping_entry(49, Tl866Instance.EARTH, 40)
_add_mapping_entry(97, Tl866Instance.WIND, 1)
_add_mapping_entry(101, Tl866Instance.WIND, 2)
_add_mapping_entry(105, Tl866Instance.WIND, 3)
_add_mapping_entry(109, Tl866Instance.WIND, 4)
_add_mapping_entry(113, Tl866Instance.WIND, 5)
_add_mapping_entry(117, Tl866Instance.WIND, 6)
_add_mapping_entry(121, Tl866Instance.WIND, 7)
_add_mapping_entry(125, Tl866Instance.WIND, 8)
_add_mapping_entry(129, Tl866Instance.WIND, 9)
_add_mapping_entry(133, Tl866Instance.WIND, 10)
_add_mapping_entry(135, Tl866Instance.WIND, 11)
_add_mapping_entry(137, Tl866Instance.WIND, 12)
_add_mapping_entry(139, Tl866Instance.WIND, 13)
_add_mapping_entry(87, Tl866Instance.WIND, 14)
_add_mapping_entry(89, Tl866Instance.WIND, 15)
_add_mapping_entry(91, Tl866Instance.WIND, 16)
_add_mapping_entry(93, Tl866Instance.WIND, 17)
_add_mapping_entry(95, Tl866Instance.WIND, 18)
_add_mapping_entry(153, Tl866Instance.WIND, 19)
_add_mapping_entry(157, Tl866Instance.WIND, 20)
_add_mapping_entry(159, Tl866Instance.WIND, 21)
_add_mapping_entry(155, Tl866Instance.WIND, 22)
_add_mapping_entry(151, Tl866Instance.WIND, 23)
_add_mapping_entry(149, Tl866Instance.WIND, 24)
_add_mapping_entry(147, Tl866Instance.WIND, 25)
_add_mapping_entry(145, Tl866Instance.WIND, 26)
_add_mapping_entry(143, Tl866Instance.WIND, 27)
_add_mapping_entry(141, Tl866Instance.WIND, 28)
_add_mapping_entry(85, Tl866Instance.WIND, 29)
_add_mapping_entry(83, Tl866Instance.WIND, 30)
_add_mapping_entry(81, Tl866Instance.WIND, 31)
_add_mapping_entry(131, Tl866Instance.WIND, 32)
_add_mapping_entry(127, Tl866Instance.WIND, 33)
_add_mapping_entry(123, Tl866Instance.WIND, 34)
_add_mapping_entry(119, Tl866Instance.WIND, 35)
_add_mapping_entry(115, Tl866Instance.WIND, 36)
_add_mapping_entry(111, Tl866Instance.WIND, 37)
_add_mapping_entry(107, Tl866Instance.WIND, 38)
_add_mapping_entry(103, Tl866Instance.WIND, 39)
_add_mapping_entry(99, Tl866Instance.WIND, 40)
_add_mapping_entry(48, Tl866Instance.FIRE, 1)
_add_mapping_entry(44, Tl866Instance.FIRE, 2)
_add_mapping_entry(40, Tl866Instance.FIRE, 3)
_add_mapping_entry(36, Tl866Instance.FIRE, 4)
_add_mapping_entry(32, Tl866Instance.FIRE, 5)
_add_mapping_entry(28, Tl866Instance.FIRE, 6)
_add_mapping_entry(26, Tl866Instance.FIRE, 7)
_add_mapping_entry(24, Tl866Instance.FIRE, 8)
_add_mapping_entry(76, Tl866Instance.FIRE, 9)
_add_mapping_entry(74, Tl866Instance.FIRE, 10)
_add_mapping_entry(72, Tl866Instance.FIRE, 11)
_add_mapping_entry(70, Tl866Instance.FIRE, 12)
_add_mapping_entry(68, Tl866Instance.FIRE, 13)
_add_mapping_entry(10, Tl866Instance.FIRE, 14)
_add_mapping_entry(8, Tl866Instance.FIRE, 15)
_add_mapping_entry(6, Tl866Instance.FIRE, 16)
_add_mapping_entry(4, Tl866Instance.FIRE, 17)
_add_mapping_entry(2, Tl866Instance.FIRE, 18)
_add_mapping_entry(56, Tl866Instance.FIRE, 19)
_add_mapping_entry(52, Tl866Instance.FIRE, 20)
_add_mapping_entry(50, Tl866Instance.FIRE, 21)
_add_mapping_entry(54, Tl866Instance.FIRE, 22)
_add_mapping_entry(58, Tl866Instance.FIRE, 23)
_add_mapping_entry(60, Tl866Instance.FIRE, 24)
_add_mapping_entry(62, Tl866Instance.FIRE, 25)
_add_mapping_entry(64, Tl866Instance.FIRE, 26)
_add_mapping_entry(66, Tl866Instance.FIRE, 27)
_add_mapping_entry(12, Tl866Instance.FIRE, 28)
_add_mapping_entry(14, Tl866Instance.FIRE, 29)
_add_mapping_entry(16, Tl866Instance.FIRE, 30)
_add_mapping_entry(18, Tl866Instance.FIRE, 31)
_add_mapping_entry(20, Tl866Instance.FIRE, 32)
_add_mapping_entry(22, Tl866Instance.FIRE, 33)
_add_mapping_entry(78, Tl866Instance.FIRE, 34)
_add_mapping_entry(80, Tl866Instance.FIRE, 35)
_add_mapping_entry(30, Tl866Instance.FIRE, 36)
_add_mapping_entry(34, Tl866Instance.FIRE, 37)
_add_mapping_entry(38, Tl866Instance.FIRE, 38)
_add_mapping_entry(42, Tl866Instance.FIRE, 39)
_add_mapping_entry(46, Tl866Instance.FIRE, 40)
_add_mapping_entry(158, Tl866Instance.WATER, 1)
_add_mapping_entry(154, Tl866Instance.WATER, 2)
_add_mapping_entry(96, Tl866Instance.WATER, 3)
_add_mapping_entry(94, Tl866Instance.WATER, 4)
_add_mapping_entry(92, Tl866Instance.WATER, 5)
_add_mapping_entry(90, Tl866Instance.WATER, 6)
_add_mapping_entry(88, Tl866Instance.WATER, 7)
_add_mapping_entry(140, Tl866Instance.WATER, 8)
_add_mapping_entry(138, Tl866Instance.WATER, 9)
_add_mapping_entry(136, Tl866Instance.WATER, 10)
_add_mapping_entry(134, Tl866Instance.WATER, 11)
_add_mapping_entry(130, Tl866Instance.WATER, 12)
_add_mapping_entry(126, Tl866Instance.WATER, 13)
_add_mapping_entry(122, Tl866Instance.WATER, 14)
_add_mapping_entry(118, Tl866Instance.WATER, 15)
_add_mapping_entry(114, Tl866Instance.WATER, 16)
_add_mapping_entry(110, Tl866Instance.WATER, 17)
_add_mapping_entry(106, Tl866Instance.WATER, 18)
_add_mapping_entry(102, Tl866Instance.WATER, 19)
_add_mapping_entry(98, Tl866Instance.WATER, 20)
_add_mapping_entry(100, Tl866Instance.WATER, 21)
_add_mapping_entry(104, Tl866Instance.WATER, 22)
_add_mapping_entry(108, Tl866Instance.WATER, 23)
_add_mapping_entry(112, Tl866Instance.WATER, 24)
_add_mapping_entry(116, Tl866Instance.WATER, 25)
_add_mapping_entry(120, Tl866Instance.WATER, 26)
_add_mapping_entry(124, Tl866Instance.WATER, 27)
_add_mapping_entry(128, Tl866Instance.WATER, 28)
_add_mapping_entry(132, Tl866Instance.WATER, 29)
_add_mapping_entry(82, Tl866Instance.WATER, 30)
_add_mapping_entry(84, Tl866Instance.WATER, 31)
_add_mapping_entry(86, Tl866Instance.WATER, 32)
_add_mapping_entry(142, Tl866Instance.WATER, 33)
_add_mapping_entry(144, Tl866Instance.WATER, 34)
_add_mapping_entry(146, Tl866Instance.WATER, 35)
_add_mapping_entry(148, Tl866Instance.WATER, 36)
_add_mapping_entry(150, Tl866Instance.WATER, 37)
_add_mapping_entry(152, Tl866Instance.WATER, 38)
_add_mapping_entry(156, Tl866Instance.WATER, 39)
_add_mapping_entry(160, Tl866Instance.WATER, 40)

all_earth_pins = []
all_water_pins = []
all_fire_pins = []
all_wind_pins = []
all_pins = []

for k, v in pin2Tl866_map.items():
    all_pins.append(k)
    if v.instance == Tl866Instance.EARTH:
        all_earth_pins.append(k)
    elif v.instance == Tl866Instance.WATER:
        all_water_pins.append(k)
    elif v.instance == Tl866Instance.FIRE:
        all_fire_pins.append(k)
    elif v.instance == Tl866Instance.WIND:
        all_wind_pins.append(k)
    else:
        raise Exception("WTF")

all_earth_pins = frozenset(all_earth_pins)
all_water_pins = frozenset(all_water_pins)
all_fire_pins = frozenset(all_fire_pins)
all_wind_pins = frozenset(all_wind_pins)
all_pins = frozenset(all_pins)

class GpioController:
    def __init__(
        self,
        water_serial_device: Optional[str] = None,
        earth_serial_device: Optional[str] = None,
        fire_serial_device: Optional[str] = None,
        wind_serial_device: Optional[str] = None,
    ) -> None:
        self.bitbangers: List[Bitbang] = []

        def add_device(self, device: Optional[str], instance: Tl866Instance):
            if device is not None:
                bb = Bitbang(device=device)
                bb.instance = instance
                bb.Tl866Pin2megaPin = Tl866Pin2megaPin_map[instance]
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
                    pins_per_tl866[pin2Tl866_map[i + 1].bitbanger] |= (
                        1 << pin2Tl866_map[i + 1].pin - 1
                    )
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

    def io_trir(self, val: int = int("ff" * 5 * 4, base=16)) -> int:
        res = 0
        for controller in self:
            pins = controller.io_trir()
            for i in range(0, TL866_HIGHEST_PIN_NUMBER):
                if pins & (1 << i):
                    res |= 1 << (controller.Tl866Pin2megaPin[i + 1] - 1)
        return res

    def io_w(self, val: int) -> None:
        for controller, val in self._get_pins_per_controller(val).items():
            controller.io_w(val)

    def io_r(self, val: int = int("ff" * 5 * 4, base=16)) -> int:
        res = 0
        for controller in self:
            pins = controller.io_r()
            for i in range(0, TL866_HIGHEST_PIN_NUMBER):
                if pins & (1 << i):
                    res |= 1 << (controller.Tl866Pin2megaPin[i + 1] - 1)
        return res

    def init(self) -> None:
        for controller in self:
            controller.init()


def debug_print_pins(pins: int):
    for i in range(0, MEGA866_HIGHEST_PIN_NUMBER):
        if pins & (1 << i):
            print(f"{i + 1:2d} ", end="")
    print()


def main() -> None:
    """
    # This turns on 9.9v across pins 1 and 4 on a single controller
    controller = GpioController(earth_serial_device="/dev/serial/by-id/usb-ProgHQ_Open-TL866_Programmer_92DD659470E765C58847A4DA-if00")
    controller.vpp_pins((1 << 50))
    controller.vpp_volt(0)
    controller.vpp_en()
    controller.vdd_en()
    controller.gnd_pins((1 << 2))
    """
    pass


if __name__ == "__main__":
    main()
