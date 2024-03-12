#!/usr/bin/env python3
import cv2
import rospy
from cv_bridge import CvBridge,CvBridgeError
from sensor_msgs.msg import Image
import PySimpleGUI as sg

def image_sub_callback(msg):
    global imgbytes
    cvbridge= CvBridge()
    try:
        cv_image = cvbridge.imgmsg_to_cv2(msg, "bgr8")
    except CvBridgeError as e:
        print(e)
    cv_image = cv2.resize(cv_image, (300, 300))
    imgbytes = cv2.imencode('.png',img=cv_image)[1].tobytes()
    
    # print("receive image")
    
list = [1,2,3,4,5]
img=cv2.imread("/home/lxn/keshe4/dof_ws/src/dofbot/datasets/0.jpg")
#使用sg显示图片img
layout = [[sg.Image(key='-IMAGE-',size=(300,300))],
          [sg.Drop(list,default_value=list[0],key='-LIST-',size=(10,1))],
          ]
window = sg.Window("python GUI", layout=layout)
img = cv2.resize(img,(300,300))
imgbytes = cv2.imencode('.png',img=img)[1].tobytes()
rospy.init_node('ui', anonymous=True)
rospy.loginfo("init node ui")
image_sub = rospy.Subscriber("/raw_image", Image, image_sub_callback, queue_size=1)

#显示图片
while True:
        event, values = window.read(timeout=20)
        if event == 'Exit' or event == sg.WIN_CLOSED:
            break
        # if event == '-LIST-':
        print(values['-LIST-'])
        window['-IMAGE-'].update(data=imgbytes)
        
window.close()



