import time

from RPi import GPIO
from utils import set_energy

LED_FREQUENCY = 2
YELLOW_LED_FREQUENCY = 1

led_pins = {
    'red': 2,
    'yellow': 3,
    'green': 4
}

GPIO.setmode(GPIO.BCM)

for pin in led_pins.values():
    GPIO.setup(pin, GPIO.OUT)
    set_energy(pin, False)

try:
    while True:
        set_energy(led_pins['red'], True)
        time.sleep(LED_FREQUENCY)

        set_energy(led_pins['yellow'], True)
        time.sleep(YELLOW_LED_FREQUENCY)

        set_energy(led_pins['red'], False)
        set_energy(led_pins['yellow'], False)

        set_energy(led_pins['green'], True)
        time.sleep(LED_FREQUENCY)
        set_energy(led_pins['green'], False)

        set_energy(led_pins['yellow'], True)
        time.sleep(YELLOW_LED_FREQUENCY)
        set_energy(led_pins['yellow'], False)
except KeyboardInterrupt:
    GPIO.cleanup()