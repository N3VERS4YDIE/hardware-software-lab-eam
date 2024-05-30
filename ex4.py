from RPi import GPIO
from colorama import Fore

BUTTON1 = 23
BUTTON2 = 24

LED1 = 2
LED2 = 3

RESULT_LED = 27

out_pins = (LED1, LED2, RESULT_LED)

current_msg = ""
last_msg = ""

GPIO.setmode(GPIO.BCM)

GPIO.setup(BUTTON1, GPIO.IN)
GPIO.setup(BUTTON2, GPIO.IN)

for pin in out_pins:
    GPIO.setup(pin, GPIO.OUT)

GPIO.setup(BUTTON1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(BUTTON2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


try:
    while True:
        button1 = GPIO.input(BUTTON1)
        button2 = GPIO.input(BUTTON2)

        GPIO.output(LED1, button1)
        GPIO.output(LED2, button2)

        binary_sum = button1 ^ button2
        GPIO.output(RESULT_LED, binary_sum)

        current_msg = f"BUTTON 1: {button1}, BUTTON 2: {button2}, RESULT: {binary_sum}"
        if current_msg != last_msg:
            color = Fore.GREEN if binary_sum else Fore.RED
            print(color + current_msg)
            last_msg = current_msg
except KeyboardInterrupt:
    GPIO.cleanup()
