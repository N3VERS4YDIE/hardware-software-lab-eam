import random
import time

from RPi import GPIO
from colorama import Fore
from utils import set_energy

BUTTON_ENERGY1 = 14
BUTTON_ENERGY2 = 15

NAVIGATION_BUTTON = 23
SELECT_BUTTON = 24

led_pins = (2, 3, 4, 17, 27)
button_pins = (NAVIGATION_BUTTON, SELECT_BUTTON)

out_pins = (BUTTON_ENERGY1, BUTTON_ENERGY2, *led_pins)


pattern = []
user_pattern = []

is_user_turn = False

current_led_index = -1
last_led_index = -1

score = 0


def config_raspberry():
    GPIO.setmode(GPIO.BCM)

    for pin in out_pins:
        GPIO.setup(pin, GPIO.OUT)

    for button in button_pins:
        GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    GPIO.add_event_detect(NAVIGATION_BUTTON, GPIO.RISING, callback=navigate, bouncetime=200)
    GPIO.add_event_detect(SELECT_BUTTON, GPIO.RISING, callback=select, bouncetime=200)

    set_energy(BUTTON_ENERGY1, True)
    set_energy(BUTTON_ENERGY2, True)

    turn_off_leds()
    play_lighting_pattern(True)
    

def navigate(pin: int):
    if is_user_turn:
        global current_led_index, last_led_index

        current_led_index += 1

        if current_led_index >= len(led_pins):
            current_led_index = 0

        current_led = led_pins[current_led_index]
        spot_led(current_led)
        last_led_index = current_led_index

def select(pin: int):
    global is_user_turn

    if is_user_turn:
        global current_led_index, score
        
        current_led = led_pins[current_led_index]
        user_pattern.append(current_led)
        turn_off_leds()

        is_pattern_valid = verify_pattern()
        if is_pattern_valid:
            score += len(user_pattern)
            print(Fore.GREEN + f"Score: {score}")
        else:
            game_over()

        if len(user_pattern) >= len(pattern):
            play_lighting_pattern(is_pattern_valid)
            
            user_pattern.clear()
            is_user_turn = False    
        
        current_led_index = -1

def spot_led(pin: int):
    turn_off_leds()
    set_energy(pin, True, False)

def turn_off_leds():
    for led in led_pins:
        set_energy(led, False, False)


def play_lighting_pattern(is_pattern_good: bool):
    turn_off_leds()
    for _ in range(3):
        for led in led_pins if is_pattern_good else reversed(led_pins):
            set_energy(led, True, False)
            time.sleep(0.1)
            set_energy(led, False, False)
            
    
    time.sleep(0.5)

def verify_pattern():
    for user_led, led in zip(user_pattern, pattern):
        if user_led != led:
            return False
    return True

def game_over():
    global score

    pattern.clear()
    score = 0

    print(Fore.RED + "\nGAME OVER")
    print(Fore.RESET + "Restarting...\n")
    play_lighting_pattern(True) 


try:
    config_raspberry()

    while True:
        if not is_user_turn:
            random_led = random.choice(led_pins)
            pattern.append(random_led)
            print(Fore.BLUE + "Pattern: ", [led_pins.index(led) + 1 for led in pattern])

            for led in pattern:
                set_energy(led, True, False)
                time.sleep(0.3)
                set_energy(led, False, False)
                time.sleep(0.1)

            is_user_turn = True
except KeyboardInterrupt:
    GPIO.cleanup()