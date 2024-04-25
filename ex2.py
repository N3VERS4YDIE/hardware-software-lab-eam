import time

from RPi import GPIO
from utils import set_energy

LED_FREQUENCY = 0.5
led_pins = (4, 17, 27, 22)

GPIO.setmode(GPIO.BCM)

for pin in led_pins:
    GPIO.setup(pin, GPIO.OUT)
    set_energy(pin, False)

try:
    while True:
        for pin in led_pins:
            set_energy(pin, True)
            time.sleep(LED_FREQUENCY)
            set_energy(pin, False)
except KeyboardInterrupt:
    GPIO.cleanup()