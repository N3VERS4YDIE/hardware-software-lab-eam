import paho.mqtt.client as mqtt
from RPi import GPIO
from online_config import connect_client
from controller_state import ControllerState

client: mqtt.Client

SELECT_BUTTON = 23
i = 0


def select(pin: int):
    client.publish(ControllerState.SELECT.name, ControllerState.SELECT.value)

    global i
    i += 1
    print(f'{ControllerState.SELECT.name} {i}')


if __name__ == "__main__":
    try:
        client = connect_client()

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(SELECT_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(SELECT_BUTTON, GPIO.RISING, callback=select)

        client.loop_forever()
    except KeyboardInterrupt:
        GPIO.cleanup()
        client.disconnect()
