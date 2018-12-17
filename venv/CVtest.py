import cv2
import numpy as np
import requests
import json

request = requests.get("http://www.005.tv/uploads/allimg/181106/49-1Q106135413301.jpg")
img_data = request.content
img_path = './test.png'
image2 = cv2.imread(img_path)

image = cv2.imdecode(np.fromstring(img_data, np.uint8), cv2.COLOR_GRAY2BGR)

image_center = [image.shape[1]/2,image.shape[0]/2]


face_cascade = cv2.CascadeClassifier(r'./haarcascade_frontalface_default.xml')

faces = face_cascade.detectMultiScale(
    image,
    scaleFactor=1.15,
    minNeighbors=5,
    minSize=(5, 5),
)

if not faces:
    print("faces null")
else :
    print("faces exist")

print(faces)


face_x :int
face_y :int
pos_x :int
pos_y :int
# 直接求出相对距离，判断正负即可控制具体的转向
# 相对距离的多少决定了转向的大小
# x为正就向左边，y为正就向上面
# for (x,y,w,h) in faces:
#     face_x = (x+w)/2
#     face_y = (y+h)/2
#     pos_x = face_x - image_center[0]
#     pos_y = face_y - image_center[1]
#
# NeckControl = [{"L_R":pos_x,"U_D":pos_y}]
# NeckControl_json = json.dumps(NeckControl)
#
