#!/usr/bin/env python3

import paho.mqtt.client as mqtt
import datetime
import argparse
import json

# define MQTT parameters
BROKER = 'broker.hivemq.com'
MQTT_HOST = BROKER
MQTT_PORT = 1883
MQTT_KEEPALIVE = 30
MQTT_TOPIC = 'ioThinx_4510/write/#'

class MQTT(mqtt.Client):

    def on_connect(self, mqttc, obj, rc):
        mqttc.subscribe(MQTT_TOPIC, 0)

    def on_message(self, mqttc, obj, msg):
        print(msg.topic + " " + "Payload: " + str(msg.payload) + " Timestamp: "
              + currentTime.strftime("%Y-%m-%d %H:%M:%S"))
#
    def on_subscribe(self, mqttc, client, userdata, result):
        print("Subscribed to " + MQTT_TOPIC)

    def on_publish(self, mqttc, obj, mid):
        print("Data published...")
        pass

    def run(self):
        self.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEPALIVE)
        self.subscribe(MQTT_TOPIC)

        self.publish(do_topic, do_value)

        #value = json.dumps({"value": 1})
        #self.publish("ioThinx_4510/write/45MR-2600-0@DO-00/doStatus", value)
        rc = 0
        while rc == 0:
            rc = self.loop()
            if input("Press 'q' to exit: ") == 'q':
                break
        return rc

def main():

    """
    Arguement -t corresponds to the specific DO.
        -t 00 --> DO-00
        -t 01 --> DO-01

    Argument -v corresponds to the value based on the selected DO from arguement -t.
        -v 1 --> value = 1 --> on
        -v 0 --> value = 0 --> off
    """

    global do_topic
    global do_value

    parser = argparse.ArgumentParser(description = "MQTT Publish: DO write")
    parser.add_argument("-t", "--topic", dest = "do_topic", type=str)
    parser.add_argument("-v", "--value", dest = "do_value", type=int)
    args = parser.parse_args()

    do_topic = "ioThinx_4510/write/45MR-2606-0@DO-"+args.do_topic+"/doStatus"
    do_value = json.dumps({"value":args.do_value})
    print("{} {}".format(do_topic, do_value))

    mqttc = MQTT()
    rc = mqttc.run()

if __name__ == '__main__':
    main()


