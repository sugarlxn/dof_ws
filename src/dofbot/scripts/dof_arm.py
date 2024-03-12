#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import rospy
# from Arm_Lib import Arm_Device
# from arm_control import ARM_Control
import time
import threading
from std_msgs.msg import String
from dofbot.srv import target, targetResponse, targetRequest

#话题回调函数
def arm_callback(msg):
    rospy.loginfo("receive msg: %s", msg.data)
    #TODO 控制机械臂

#服务回调函数
def arm_control(target):
    rospy.loginfo("target: %s", target)
    #TODO 控制机械臂
    # if target != None:
    #    arm_control.arm_control_from_instuction(target)
    #    time.sleep(0.01)
    time.sleep(1)

if __name__ == '__main__':
    #init ros node
    rospy.init_node('arm_control', anonymous=True)
    rospy.loginfo("init node arm_control")
    #订阅话题
    # sub = rospy.Subscriber('/arm_control', String, arm_callback)
    arm_client = rospy.ServiceProxy('/arm_server', target)
    arm_client.wait_for_service()
    #创建机械臂对象
    # arm_control = ARM_Control()
    while not rospy.is_shutdown():
        #提供服务
        res = arm_client.call(targetRequest(1))
        arm_control(res.target)
        time.sleep(0.1)
    rospy.spin()