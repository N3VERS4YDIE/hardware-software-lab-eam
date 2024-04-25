import time

from RPi import GPIO
from utils import set_energy

LED_FREQUENCY = 0.2
LED_PIN = 4

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

try:
    while True:
        set_energy(LED_PIN, True)
        time.sleep(LED_FREQUENCY)

        set_energy(LED_PIN, False)
        time.sleep(LED_FREQUENCY)

except KeyboardInterrupt:
    GPIO.cleanup()