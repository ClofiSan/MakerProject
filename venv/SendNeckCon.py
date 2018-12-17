import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import cv2
import numpy as np
import requests
import struct as s
import time
import json

Control_Topic = '888'
Get_Img_Topic = '666'

MQTTHOST = "119.23.227.254"
# MQTTHOST = "192.168.253.1"
MQTTPORT = 1883
mqttClient = mqtt.Client()


class face_detect:
    # 没有识别到人脸该怎么办
    img_data = ''
    image = ''
    image_center = []
    face_center = []
    faces = ''

    def __init__(self,img_data):
        self.img_data = img_data
        self.image = cv2.imdecode(np.fromstring(img_data, np.uint8), cv2.COLOR_GRAY2BGR)
        self.image_center = self.get_image_center(self.image)
        self.faces = self.detect_face(self.image)
        self.face_center = self.get_face_center(self.faces)

    def get_image_center(self,image):
        image_center = [image.shape[1] / 2, image.shape[0] / 2]
        return image_center

    def detect_face(self,image):
        # 假如faces没有会怎么样
        face_cascade = cv2.CascadeClassifier(r'./haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(
            image,
            scaleFactor=1.15,
            minNeighbors=5,
            minSize=(5, 5),
        )
        if faces is None:
            print("No face!")
        else :
            print("Detected Successfully")
            return faces

    def get_face_center(self,faces):
        face_center = []
        face_x:int
        face_y:int
        for (x, y, w, h) in faces:
            face_x = (x + w) / 2
            face_y = (y + h) / 2
        face_center.append(face_x)
        face_center.append(face_y)
        return face_center

    def get_neck_control(self):
        if self.faces is None:
            NeckControl = [{"Deface":0,"L_R": 0, "U_D": 0}]
        else :
            pos_x = self.face_center[0] - self.image_center[0]
            pos_y = self.face_center[1] - self.image_center[1]
            NeckControl = [{"Deface":1,"L_R": pos_x, "U_D": pos_y}]
        NeckControl_json = json.dumps(NeckControl)
        return NeckControl_json



def mqtt_connect():
    mqttClient.connect(MQTTHOST, MQTTPORT, 60)
    mqttClient.loop_start()
    print("Connect Successfully")

def on_message_come(Client, userdata, msg):
    print(msg.topic + " " + ":" + str(msg.payload))
    if msg.topic == Get_Img_Topic:
        img_data = msg.payload
        face_detect1 = face_detect(img_data)
        NeckControl = face_detect1.get_neck_control()
        NeckControl_json = json.dumps(NeckControl)
        on_publish(Control_Topic,NeckControl_json,2)



def on_publish(topic, payload, qos):
    mqttClient.publish(topic, payload, qos)
    print("Publish Successfully:"+topic+payload)


def on_subscribe(topic):
    mqttClient.subscribe(topic, 2)
    mqttClient.on_message = on_message_come
    print("Subscribe Successfully")

if __name__ == '__main__':
    mqtt_connect()
    while True:
        time.sleep(3)
        on_subscribe(Get_Img_Topic)


