import paho.mqtt.client as mqtt
from RPi import GPIO
from controller_state import ControllerState

client = mqtt.Client()

NAVIGATION_BUTTON = 23
SELECT_BUTTON = 24

button_pins = (NAVIGATION_BUTTON, SELECT_BUTTON)

is_player_turn = True

def navigate(pin: int):
    print(ControllerState.NAVIGATE.name)
    client.publish("controller_state", ControllerState.NAVIGATE.value)

def select(pin: int):
    print(ControllerState.SELECT.name)
    client.publish("controller_state", ControllerState.SELECT.value)


if __name__ == "__main__":
    try:
        client.connect("192.168.14.192", 6666)

        GPIO.setmode(GPIO.BCM)

        for button in button_pins:
            GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        GPIO.add_event_detect(
            NAVIGATION_BUTTON, GPIO.RISING, callback=navigate, bouncetime=350
        )
        GPIO.add_event_detect(SELECT_BUTTON, GPIO.RISING, callback=select, bouncetime=350)

        client.loop_forever()
    except KeyboardInterrupt:
        GPIO.cleanup()
        client.disconnect()