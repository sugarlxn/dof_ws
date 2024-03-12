#!/usr/bin/env python3
import cv2
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError


def image_write_callback(msg):
    bridge = CvBridge()
    try:
        cv_image = bridge.imgmsg_to_cv2(msg, "bgr8")
    except CvBridgeError as e:
        print(e)
    # print("write image")
    cv2.imshow('result', cv_image)
    # cv2.waitKey(3)
    if cv2.waitKey(10) & 0xFF == ord('s'):
        cv2.imwrite("../datasets/"+ str(index)+ ".jpg", cv_image)
        

if __name__=="__main__":

    rospy.init_node("image_writer")
    rospy.loginfo("dof_camera init")
    bridge = CvBridge()
    index = 0
    raw_image_sub = rospy.Subscriber("/raw_image", Image, image_write_callback, queue_size=1)
    rospy.spin()

