import os, json
import paho.mqtt.client as mqtt

def not_empty(string):
    return string != ''

def on_connect(client, userdata, flags, rc):
    client.subscribe(robot + '/#')

def on_message(client, userdata, msg):
    topic = list(filter(not_empty, msg.topic.split('/')))
    print(json.dumps({(topic[1]): str(msg.payload.decode('utf-8'))}))

if __name__ == '__main__':
    try:
        robot = os.environ['ROBOT']
    except:
        robot = 'julinho'

    try:
        broker = os.environ['MQTT_BROKER']
    except:
        broker = 'mqtt.sj.ifsc.edu.br'

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(broker, 1883, 60)
    client.loop_forever()
