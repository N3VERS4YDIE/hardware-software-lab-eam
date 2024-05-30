import random
import time

import paho.mqtt.client as mqtt
from RPi import GPIO
from colorama import Fore
from controller_state import ControllerState
from online_config import connect_client

client: mqtt.Client

led_pins = (2, 3, 4, 17, 27)

pattern = []
user_pattern = []

is_player_turn = False
led_count = -1
score = 0


def on_connect(client, userdata, flags, rc):
    client.subscribe("controller_state")


def on_message(client, userdata, msg):
    global is_player_turn

    state = int(msg.payload.decode())
    if state == ControllerState.NAVIGATE.value and is_player_turn:
        navigate()
    elif state == ControllerState.SELECT.value and is_player_turn:
        select()


def navigate():
    global led_count

    led_count += 1
    spot_led(get_current_led())


def select():
    global is_player_turn, led_count
    is_player_turn = False

    global score

    user_pattern.append(get_current_led())
    turn_off_leds()

    if not verify_pattern():
        game_over()
        return
    score += len(user_pattern)
    print(Fore.CYAN + f"Score: {score}")

    if len(user_pattern) >= len(pattern):
        is_player_turn = False
        user_pattern.clear()
        play_feedback_pattern(verify_pattern())
        computer_choice()

    led_count = 0
    spot_led(get_current_led())
    is_player_turn = True


def computer_choice():
    random_led = random.choice(led_pins)
    pattern.append(random_led)
    print(Fore.BLUE + "Pattern: ", [led_pins.index(led) + 1 for led in pattern])
    play_pattern()


def spot_led(pin: int):
    turn_off_leds()
    GPIO.output(pin, True)
    time.sleep(0.1)
    GPIO.output(pin, False)
    time.sleep(0.1)
    GPIO.output(pin, True)


def play_pattern():
    for led in pattern:
        GPIO.output(led, True)
        time.sleep(0.3)
        GPIO.output(led, False)
        time.sleep(0.1)
    time.sleep(0.5)


def play_feedback_pattern(is_pattern_good: bool):
    for _ in range(3):
        for led in led_pins if is_pattern_good else reversed(led_pins):
            GPIO.output(led, True)
            time.sleep(0.1)
            GPIO.output(led, False)
    time.sleep(0.5)


def play_starter_pattern():
    for _ in range(3):
        GPIO.output(led_pins[2], True)
        time.sleep(0.1)
        GPIO.output(led_pins[2], False)

        GPIO.output(led_pins[1], True)
        GPIO.output(led_pins[3], True)
        time.sleep(0.1)
        GPIO.output(led_pins[1], False)
        GPIO.output(led_pins[3], False)

        GPIO.output(led_pins[0], True)
        GPIO.output(led_pins[4], True)
        time.sleep(0.1)
        GPIO.output(led_pins[0], False)
        GPIO.output(led_pins[4], False)
    time.sleep(0.5)


def turn_off_leds():
    for led in led_pins:
        GPIO.output(led, False)


def verify_pattern():
    for user_led, led in zip(user_pattern, pattern):
        if user_led != led:
            return False
    return True


def get_current_led():
    return led_pins[led_count % len(led_pins)]


def start():
    global is_player_turn, led_count, score

    pattern.clear()
    user_pattern.clear()
    is_player_turn = False
    led_count = 0
    score = 0

    print(Fore.GREEN + "Starting game...")
    play_starter_pattern()
    computer_choice()
    spot_led(get_current_led())
    is_player_turn = True


def game_over():
    global score

    print(Fore.RED + "\nGAME OVER")
    print(Fore.MAGENTA + f"Total Score: {score}")
    print(Fore.RESET + "Restarting...\n")

    play_feedback_pattern(False)
    start()


if __name__ == "__main__":
    try:
        client = connect_client()
        client.on_connect = on_connect
        client.on_message = on_message

        GPIO.setmode(GPIO.BCM)

        for led in led_pins:
            GPIO.setup(led, GPIO.OUT)

        start()

        client.loop_forever()
    except KeyboardInterrupt:
        GPIO.cleanup()
