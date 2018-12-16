import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import cv2
import numpy as np
import requests
import struct as s
import time

MQTTHOST = "119.23.227.254"
MQTTPORT = 1883
mqttClient = mqtt.Client()


def mqtt_connect():
    mqttClient.connect(MQTTHOST, MQTTPORT, 60)
    mqttClient.loop_start()
    print("Connect Successfully")


def on_message_come(Client, userdata, msg):
    print(msg.topic + " " + ":" + str(msg.payload))


def on_publish(topic, payload, qos):
    mqttClient.publish(topic, payload, qos)
    print("Publish Successfully")


def on_subscribe(topic):
    mqttClient.subscribe(topic, 2)
    mqttClient.on_message = on_message_come


img_data = requests \
    .get("http://www.qipaishuo.com/uploads/allimg/140111/1-1401111J404Q0.jpg") \
    .content
image = cv2.imdecode(np.fromstring(img_data, np.uint8), cv2.COLOR_GRAY2BGR)
print(img_data)
print(image)
data = []
Format = ''
for i in range(len(img_data)):
    data.append(img_data[i])
    Format += 'B'
packed = s.pack(Format, *data)
mqtt_connect()
while True:
    time.sleep(3)
    print(packed)
    on_publish('DeFace', img_data, 2)