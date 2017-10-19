import os, json
import paho.mqtt.client as mqtt
from client import RoutesClient

def not_empty(string):
    return string != ''

def on_connect(client, userdata, flags, rc):
    client.subscribe(ROBOT + '/#')

def on_message(client, userdata, msg):
    try:
        topics = list(filter(not_empty, msg.topic.split('/')))

        if len(topics) < 2 or topics[1] not in ALLOWED_TOPICS:
            return

        topic = topics[1]

        message = str(msg.payload.decode('utf-8'))

        status = True if message == '1' else False

        routes_client.status({
            'topic': topic,
            'status': status
        })
        print(topic.upper() + ' ' + message)
    except Exception as e:
        print(e)


def main():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(BROKER, 1883, 60)
    client.loop_forever()

if __name__ == '__main__':
    ROBOT = os.getenv('ROBOT', 'julinho')
    BROKER = os.getenv('MQTT_BROKER', 'mqtt.sj.ifsc.edu.br')
    ROUTES_HOST = os.getenv('ROUTES_HOST', 'localhost')
    ROUTES_PORT = os.getenv('ROUTES_PORT', '80')
    CLIENT_ID = os.getenv('CLIENT_ID', '1')

    ALLOWED_TOPICS = ['help', 'enable', 'check']

    routes_client = RoutesClient(
        base_url='http://' + ROUTES_HOST + ':' + ROUTES_PORT,
        key_path='private.key',
        client_id=CLIENT_ID
    )

    main()
