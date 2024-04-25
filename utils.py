from RPi import GPIO
from colorama import Fore


def set_energy(pin: int, on: bool, verbose=True):
    GPIO.output(pin, GPIO.HIGH if on else GPIO.LOW)
    color = Fore.GREEN if on else Fore.RED
    state = 'ON' if on else 'OFF'

    if verbose:
        print(f'{color}LED {pin} {state}')