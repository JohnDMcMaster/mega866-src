from gpio_controller import GpioController, all_earth_pins
from time import sleep
from intelhex import IntelHex
import sys
import os
from threading import Thread, Event
from prompt_toolkit.application import Application
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout.containers import HSplit, VSplit, Window, WindowAlign
from prompt_toolkit.layout.controls import BufferControl, FormattedTextControl
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.document import Document

bus_activity_buffer = Buffer(read_only=True)
io_output_buffer = Buffer(read_only=True)


def get_left_window_title_text():
    return [
        ("class:title", "Address - Data - r/w"),
    ]

left_window = HSplit(
    [
        # The titlebar.
        Window(
            height=len(get_left_window_title_text()),
            content=FormattedTextControl(get_left_window_title_text),
            align=WindowAlign.CENTER,
        ),
        # Horizontal separator.
        Window(height=1, char="-", style="class:line"),
        # The 'body', like defined above.
        Window(BufferControl(buffer=bus_activity_buffer), wrap_lines=True)
    ]
)

def get_right_window_title_text():
    return [
        ("class:title", "Console Output"),
    ]

right_window = HSplit(
    [
        # The titlebar.
        Window(
            height=len(get_right_window_title_text()),
            content=FormattedTextControl(get_right_window_title_text),
            align=WindowAlign.CENTER,
        ),
        # Horizontal separator.
        Window(height=1, char="-", style="class:line"),
        # The 'body', like defined above.
        Window(BufferControl(buffer=io_output_buffer), wrap_lines=True)
    ]
)


body = VSplit(
    [
        left_window,
        # A vertical line in the middle. We explicitly specify the width, to make
        # sure that the layout engine will not try to divide the whole width by
        # three for all these windows.
        Window(width=1, char="|", style="class:line"),
        # Display the Result buffer on the right.
        right_window,
    ]
)

def get_titlebar_text():
    return [
        ("class:title", " 6502 Thingy\n"),
        ("class:title", " Press [Ctrl-C] to quit\n"),
        ("class:title", " Press [Enter] for one clock cycle\n"),
        ("class:title", " Press CTRL-R to run the clock freely (Press [Enter] to re-enter single-step mode)\n"),
    ]


root_container = HSplit(
    [
        # The titlebar.
        Window(
            height=len(get_titlebar_text()),
            content=FormattedTextControl(get_titlebar_text),
            align=WindowAlign.CENTER,
        ),
        # Horizontal separator.
        Window(height=1, char="-", style="class:line"),
        # The 'body', like defined above.
        body,
    ]
)

kb = KeyBindings()

@kb.add("c-c", eager=True)
def _(event):
    stop_event.set()
    try:
        free_run_thread.join()
    except:
        pass
    event.app.exit()

def clock_loop():
    while stop_event.is_set() is False:
            clock_cycle_and_display()

free_run_thread = Thread(target=clock_loop)
stop_event = Event()

@kb.add("c-r", eager=True)
def _(event):
    global free_run_thread
    stop_event.clear()
    if free_run_thread.is_alive() is False:
        free_run_thread = Thread(target=clock_loop)
        free_run_thread.start()

@kb.add("enter", eager=True)
def _(event):
    if free_run_thread.is_alive():
        stop_event.set()
    else:
        clock_cycle_and_display()

# 3. Creating an `Application` instance
#    ----------------------------------

# This glues everything together.

application = Application(
    layout=Layout(root_container, focused_element=left_window),
    key_bindings=kb,
    full_screen=True,
)


def run():
    # Run the interface. (This runs the event loop until Ctrl-Q is pressed.)
    application.run()



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

# NOTE: pin 45 needs to be conencted to ground manually using a jumper wire or the like.

# We assume one attached tl866 and we call it the "earth" controller
c = GpioController(
    earth_serial_device="/dev/serial/by-id/usb-ProgHQ_Open-TL866_Programmer_33144A91666856D18E6084EC-if00"
)

tristate_pins = set(all_earth_pins)

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
data_pins_rev = {}
for k, v in data_pins.items():
    data_pins_rev[v] = k

def set_data_pins_high_z():
    global tristate_pins
    tristate_pins |= set(data_pins.keys())
    c.io_tri(pins(*tristate_pins))

def set_data_pins_rw():
    global tristate_pins
    tristate_pins -= set(data_pins.keys())
    c.io_tri(pins(*tristate_pins))

def get_data_pins_from_byte(b):
    pins = []
    for i in range(0, 8):
        if (1 << i) & b:
            pins.append(data_pins_rev[i])
    return pins

set_data_pins_high_z()

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

memory = {}

ih = IntelHex(os.path.join(os.path.realpath(os.path.dirname(__file__)), 'prog_6502.hex'))

for addr in ih.addresses():
    memory[addr] = ih[addr]

OUT_PORT = 0x6000
WRITE = 0
READ = 1

def handle_write(address, data):
    if address == OUT_PORT:
        io_output_buffer.set_document(
        io_output_buffer.document.insert_after(chr(data)), bypass_readonly=True)
        io_output_buffer.auto_down()
    else:
        memory[address] = data

def handle_read(address):
    return memory.get(address, 0)

c.init()
c.io_tri(pins(*tristate_pins))

always_high_pins = pins(3, 7, 49, 55, 57, 61)

c.vdd_volt(1)  # 3.5V
c.vdd_pins(pins(67))  # VDD
c.vdd_en()

c.io_w(0)  # This should reset the 6502
sleep(0.001)
# First rising edge starts reset sequence
c.io_w(always_high_pins | pin(CLOCK_PIN))
sleep(0.001)
c.io_w(always_high_pins)

def clock_cycle():
    set_data_pins_high_z()
    sleep(0.0000003)
    input_pins = c.io_r()
    address = get_address_pins(input_pins)
    rw = get_rw_pin(input_pins)
    data = 0
    if rw == READ:
        set_data_pins_rw()
        data = handle_read(address)
        c.io_w(always_high_pins | pins(*get_data_pins_from_byte(data)) | pin(CLOCK_PIN))
        sleep(0.0000003)
        c.io_w(always_high_pins | pins(*get_data_pins_from_byte(data)))
    else:
        c.io_w(always_high_pins | pin(CLOCK_PIN))
        sleep(0.0000003)
        input_pins = c.io_r()
        data = get_data_pins(input_pins)
        handle_write(address, data)
        c.io_w(always_high_pins)
        sleep(0.0000003)

    return f"{address:#06x} {data:#04x} {'r' if rw == 1 else 'w'}\n"

def clock_cycle_and_display():
    bus_str = clock_cycle()
    bus_activity_buffer.set_document(
    bus_activity_buffer.document.insert_after(bus_str), bypass_readonly=True)
    bus_activity_buffer.auto_down()


if __name__ == "__main__":
    run()

