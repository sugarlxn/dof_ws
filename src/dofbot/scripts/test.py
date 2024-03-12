#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import rospy
import time
from std_msgs.msg import String
# import pandas as pd


# rospy.init_node('test', anonymous=True)
# rospy.loginfo("init node test")
# test_pub = rospy.Publisher('/test', String, queue_size=1)
# rate = rospy.Rate(1)

# while not rospy.is_shutdown():
#     test_pub.publish("[480.44879150390625, 0.0, 640.0, 359.1475830078125, 0.5728760957717896, 0, 'face']")
#     rate.sleep()
target = "[480.44879150390625, 0.0, 640.0, 359.1475830078125, 0.5728760957717896, 0, 'face']"
target_list = eval(target)
print(type(target_list))
print("class:",target_list[-1])

# index =1

# def add():
#     global index
#     print(index)
#     index=0
#     print(index)
# add()
# print(index)


