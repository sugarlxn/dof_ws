#!/usr/bin/env python3
import torch
import cv2
import time
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from std_msgs.msg import String

target_transform = {"OK": "Ok","diss":"Thumb_down","5.0":"Five","7.0":"Seven","heart":"Heart_single","7":"Seven","5":"Five"}
target_count={"index":None,"counts":0}


def is_send_target(target_list):
    #统计target_list[-2]的index连续出现的次数
    if(target_count["index"]==target_list[-2] or target_count["index"]==None):
        target_count["index"]=target_list[-2]
        target_count["counts"]+=1
    else:
        target_count["index"]=target_list[-2]
        target_count["counts"]=1
    #如果连续出现的次数大于5次，则认为识别成功
    if(target_count["counts"]>1):
        target_count["index"]=None
        target_count["counts"]=0
        return True
    #否则，识别失败
    else:
        return False


def translate(target_list):
    # if(target_list[-1] in target_transform.keys()):
    target_list[-1] = target_transform[str(target_list[-1])]
    return target_list

def image_sub_callback(msg):
    global time_last
    tiem_now = rospy.Time.now()
    fps = 1/(tiem_now - time_last).to_sec()
    time_last = tiem_now
    # rospy.loginfo("fps: %f", fps)

    bridge = CvBridge()
    try:
        cv_image = bridge.imgmsg_to_cv2(msg, "bgr8")
    except CvBridgeError as e:
        print(e)
    cv_image = cv2.resize(cv_image, (640, 640))
    results = model(cv_image[:,:,::-1], size=640)
    # Results
    # print(results.pandas().xyxy[0].sort_values('confidence')) # or .show(), .save(), .crop(), .pandas(), etc.
    target = results.pandas().xyxy[0].sort_values('confidence').values.tolist()
    if len(target) > 0:
        #target[0]: [480.44879150390625, 0.0, 640.0, 359.1475830078125, 0.5728760957717896, 0, 'face']
        # print("target:", target[0])
        target = translate(target_list=target[0])
        if(is_send_target(target)):
            result_pub.publish(str(target))
            print("target:",target)
        else:
            result_pub.publish("[0,0,0,0,0,0,'none']")
    else:
        # result_pub.publish("[0,0,0,0,0,0,'none']")
        # print([0.0,0.0,0.0,0.0,0.0,0.0,0,'无'])
        pass

    img = results.render()
    cv2.putText(img[0], "fps: {:.2f}".format(fps), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    try:
        measges_image = bridge.cv2_to_imgmsg(img[0][:,:,::-1], "bgr8")
        image_pub.publish(measges_image)
    except CvBridgeError as e:
        print(e)
    # cv2.imshow('result', img[0][:,:,::-1])
    # cv2.waitKey(3)
    # img = img[0][:,:,::-1]
    # image_pub.publish(bridge.cv2_to_imgmsg(img, "bgr8"))
    # arm_pub.publish(str(target[-1][-1]))
    

if __name__ == '__main__':

    # Model path:/home/lxn/keshe4/dof_ws/src/dofbot/scripts/best.pt
    model = torch.hub.load('/home/lxn/YOLO/yolov5', 'custom', path='/home/lxn/keshe4/dof_ws/src/dofbot/scripts/bestv2.pt', source='local') # or yolov5n - yolov5x6, custom
    # Images
    path = "/home/lxn/YOLO/datasets/temp/tian.jpg"  # or file, Path, PIL, OpenCV, numpy, list

    
    #init ros node
    rospy.init_node('yolov5_detect', anonymous=True)
    rospy.loginfo("init node yolov5_detect")
    #获取时间戳
    time_last = rospy.Time.now()
    image_pub = rospy.Publisher('/image_result', Image, queue_size=1)
    result_pub = rospy.Publisher('/detect_result', String, queue_size=1)
    image_sub = rospy.Subscriber("/raw_image", Image, image_sub_callback, queue_size=1)
    # arm_server = rospy.Service('/arm_server', target, arm_callback)

    rospy.spin()




    # rate = rospy.Rate(10)
    # bridge = CvBridge()
    # target = []

    # while not rospy.is_shutdown():
    #     img = cv2.imread(path)[:,:,::-1]
    #     results = model(img, size=640)
    #     # Results
    #     # print(results.pandas().xyxy[0].sort_values('confidence')) # or .show(), .save(), .crop(), .pandas(), etc.
    #     target = results.pandas().xyxy[0].sort_values('confidence').values.tolist()
    #     # print("target:",target[-1])
    #     img = results.render()
    #     cv2.imshow('result', img[0][:,:,::-1])
    #     # img = img[0][:,:,::-1]
    #     # image_pub.publish(bridge.cv2_to_imgmsg(img, "bgr8"))
    #     # arm_pub.publish(str(target[-1][-1]))

    #     rate.sleep()

