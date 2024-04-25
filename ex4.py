from RPi import GPIO
from colorama import Fore
from utils import set_energy

BUTTON_ENERGY1 = 14
BUTTON_ENERGY2 = 15

BUTTON1 = 23
BUTTON2 = 24

LED1 = 2
LED2 = 3

RESULT_LED = 27

out_pins = (BUTTON_ENERGY1, BUTTON_ENERGY2, LED1, LED2, RESULT_LED)

current_msg = ""
last_msg = ""


GPIO.setmode(GPIO.BCM)

GPIO.setup(BUTTON1, GPIO.IN)
GPIO.setup(BUTTON2, GPIO.IN)

for pin in out_pins:
    GPIO.setup(pin, GPIO.OUT)


try:
    set_energy(BUTTON_ENERGY1, True)
    set_energy(BUTTON_ENERGY2, True)

    while True:
        button1 = int(not GPIO.input(BUTTON1))
        button2 = int(not GPIO.input(BUTTON2))

        set_energy(LED1, button1, False)
        set_energy(LED2, button2, False)

        binary_sum = button1 ^ button2
        set_energy(RESULT_LED, binary_sum, False)

        current_msg = f"BUTTON 1: {button1}, BUTTON 2: {button2}, RESULT: {binary_sum}"
        if current_msg != last_msg:
            color = Fore.GREEN if binary_sum else Fore.RED
            print(color + current_msg)
            last_msg = current_msg
except KeyboardInterrupt:
    GPIO.cleanup()