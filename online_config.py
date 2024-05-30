import paho.mqtt.client as mqtt

BROKER = '192.168.219.192'
GAME_RASPBERRY = '192.168.219.231'
CONTROLLER_RASPBERRY = '192.168.219.183'


def connect_client() -> mqtt.Client:
    client = mqtt.Client()
    client.connect(BROKER, 6666)
    return client
