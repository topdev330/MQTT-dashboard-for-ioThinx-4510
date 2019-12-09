#!/usr/bin/env python3

import paho.mqtt.client as mqtt
import datetime
import json

# define MQTT parameters
BROKER = '35.157.173.121'
MQTT_HOST = BROKER
MQTT_PORT = 1883
MQTT_KEEPALIVE = 30
MQTT_TOPIC = 'ioThinx_4510/#'


class MQTT(mqtt.Client):

    def on_connect(self, mqttc, obj, rc):
        # subscribe
        mqttc.subscribe(MQTT_TOPIC, 0)

    def on_message(self, mqttc, obj, msg):
        # define timestap and print new msg
        now = datetime.datetime.now()
        print(msg.topic + " " + "Payload: " + str(msg.payload))

        #+ " Timestamp: " + str(now ))

    def on_subscribe(self, mqttc, obj, mid, granted_qos):
        # subscribe succesful
        print("Subscribed to " + MQTT_TOPIC)

    def run(self):
        # Connect to broker
        self.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEPALIVE)
        self.subscribe(MQTT_TOPIC)

        rc = 0
        while rc == 0:
            rc = self.loop()
        return rc

if __name__ == '__main__':
    # Initiate MQTT Client
    mqttc = MQTT()
    rc = mqttc.run()

