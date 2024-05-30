import random
import time
from threading import Thread

import paho.mqtt.client as mqtt
from RPi import GPIO
from colorama import Fore
from online_config import connect_client
from controller_state import ControllerState

client: mqtt.Client

WINNER_ALERT_LED = 22
led_pins = (2, 3, 4, 17, 27, WINNER_ALERT_LED)

winner_led = 0
current_led = 0

is_player_turn = False

MIN_SPEED = 2
MAX_SPEED = 8
speed = MIN_SPEED

MIN_SCORE = 1
score = MIN_SCORE


def on_connect(client, userdata, flags, rc):
    client.subscribe(ControllerState.SELECT.name)


def on_message(client, userdata, msg):
    global is_player_turn
    is_player_turn = False


def verify_win():
    global speed, score
    if current_led == winner_led:
        if speed < MAX_SPEED:
            speed += 0.5
        score += speed * 2

        print(Fore.RED + '\nU Win!!!')
        play_feedback_pattern(True)
    else:
        play_feedback_pattern(False)
        speed = MIN_SPEED
        score = MIN_SCORE

    print(Fore.RESET + 'Restarting...\n')


def computer_choice():
    global winner_led
    winner_led = random.choice(led_pins)
    print(Fore.MAGENTA + 'Winner led: ', led_pins.index(winner_led) + 1)
    alert_winner_led()


def play_pattern():
    global current_led
    for led in led_pins:
        current_led = led

        turn_off_leds()
        GPIO.output(led, True)
        time.sleep(1 / speed)

        if not is_player_turn:
            print(Fore.CYAN + 'Selected led: ', led_pins.index(led) + 1)
            spot_led(led)
            break


def turn_off_leds():
    for led in led_pins:
        GPIO.output(led, False)


def spot_led(pin: int):
    GPIO.output(pin, False)
    time.sleep(0.1)
    GPIO.output(pin, True)
    time.sleep(0.2)
    GPIO.output(pin, False)
    time.sleep(0.1)


def alert_winner_led():
    turn_off_leds()
    GPIO.output(WINNER_ALERT_LED, True)
    for _ in range(4):
        GPIO.output(winner_led, True)
        time.sleep(0.1)
        GPIO.output(winner_led, False)
        time.sleep(0.1)
    time.sleep(0.5)
    GPIO.output(WINNER_ALERT_LED, False)


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


def play_feedback_pattern(is_pattern_good: bool):
    for _ in range(3):
        for led in led_pins if is_pattern_good else reversed(led_pins):
            GPIO.output(led, True)
            time.sleep(0.1)
            GPIO.output(led, False)
    time.sleep(0.5)


def connect():
    global client
    client = connect_client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.loop_forever()


if __name__ == '__main__':
    try:
        Thread(target=connect).start()

        GPIO.setmode(GPIO.BCM)

        for led in led_pins:
            GPIO.setup(led, GPIO.OUT)

        led_pins = led_pins[:-1]

        print(Fore.GREEN + 'Starting game...')
        play_starter_pattern()

        while True:
            if is_player_turn:
                while is_player_turn:
                    play_pattern()
                verify_win()
            else:
                print(Fore.BLUE + f'Speed: {speed}')
                print(Fore.BLUE + f'Score: {score if score > 1 else 0}\n')
                computer_choice()
                is_player_turn = True
    except KeyboardInterrupt:
        GPIO.cleanup()
        client.disconnect()
