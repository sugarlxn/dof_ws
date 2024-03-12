#!/usr/bin/env python3
#-*- coding:utf-8 -*-
from Arm_Lib import Arm_Device
import time
import threading


class ARM_Control():
    def __init__(self) -> None:
        self.arm = Arm_Device()
        self.target = None
        self.action = {'look_at' : [90, 164, 18, 0, 90, 90],
                        'p_Prayer' : [90, 90, 0, 180, 90, 180],
                        'p_Thumb_up' : [90, 90, 90, 90, 90, 180], 
                        'p_Heart_single' : [90, 0, 180, 0, 90, 30], 
                        'p_Eight' : [90, 180, 18, 0, 90, 90],
                        'p_Congratulation' : [90, 131, 52, 0, 90, 180],
                        'p_Rock' : [90, 0, 90, 180, 90, 0],
                        'p_fist' : [90, 90, 0, 0, 90, 0],
                        'p_horse_1' : [90, 7, 153, 19, 0, 126], 
                        'p_horse_2' : [90, 5, 176, 0, 0, 180],
                        'p_horse_3' : [90, 62, 158, 0, 0, 0]}
        self.runing = 0
        self.arm_status = 0

    # 定义移动机械臂函数,同时控制1-6号舵机运动，p=[S1,S2,S3,S4,S5,S6]
    def arm_move_6(self,p,s_time = 500):
        for i in range(6):
            id = i + 1  
            self.arm.Arm_serial_servo_write(id, p[i], s_time)
            time.sleep(0.01)
        time.sleep(s_time/1000)

    # 定义小马运动
    def horse_running(self):
        self.arm.Arm_serial_servo_write(6, 150, 300)
        time.sleep(.3)
        self.arm.Arm_serial_servo_write(6, 180, 300)
        time.sleep(.3)
        
    
    # 根据index 机器臂响应对应的动作
    def ctrl_arm_move(self,index):
        if index == "Prayer":
            self.arm_move_6(self.action['p_Prayer'], 1000)
            time.sleep(1.5)
            self.arm_move_6(self.action['look_at'], 1000)
            time.sleep(1)
        elif index == "Thumb_up":
            s_time = 500
            self.arm.Arm_serial_servo_write(6, 180, s_time)
            time.sleep(s_time/1000)
            self.arm.Arm_serial_servo_write(6, 90, s_time)
            time.sleep(s_time/1000)
            self.arm.Arm_serial_servo_write(6, 180, s_time)
            time.sleep(s_time/1000)
            self.arm.Arm_serial_servo_write(6, 90, s_time)
            time.sleep(s_time/1000)
        elif index == "Ok":
            s_time = 300
            self.arm.Arm_serial_servo_write(4, 10, s_time)
            time.sleep(s_time/1000)
            self.arm.Arm_serial_servo_write(4, 0, s_time)
            time.sleep(s_time/1000)
            self.arm.Arm_serial_servo_write(4, 10, s_time)
            time.sleep(s_time/1000)
            self.arm.Arm_serial_servo_write(4, 0, s_time)
            time.sleep(s_time/1000)
        elif index == "Heart_single":
            self.arm_move_6([90, 90, 90, 90, 90, 90], 800)
            time.sleep(.1)
            self.arm_move_6(self.action['p_Heart_single'], 1000)
            time.sleep(1)
        elif index == "Five":
            self.arm_move_6(self.action['look_at'], 1000)
            time.sleep(.5)
        elif index == "Eight":
            s_time = 300
            self.arm_move_6(self.action['p_Eight'], 0)
            time.sleep(1)
            self.arm.Arm_serial_servo_write(2, 165, s_time)
            time.sleep(s_time/1000)
        elif index == "Rock":
            self.arm.Arm_serial_servo_write6_array(self.action['p_Rock'], 1300)
            time.sleep(3)
            self.arm.Arm_serial_servo_write6_array(self.action['look_at'], 1000)
            time.sleep(1)
        elif index == "Thumb_down": 
            self.arm.Arm_serial_servo_write6_array(self.action['p_horse_1'], 1300)
            time.sleep(1) 
        elif index == "Congratulation": 
            self.arm.Arm_serial_servo_write6_array(self.action["p_horse_2"], 1000)
            time.sleep(1)
            self.running = 1
            while self.running == 1:
                self.horse_running()
        elif index == "Seven": 
            self.arm.Arm_Buzzer_On(8)   
            self.arm.Arm_serial_servo_write6_array(self.action["p_horse_3"], 1000)
            time.sleep(2)
            self.arm.Arm_serial_servo_write6_array(self.action["look_at"], 1000)
            time.sleep(1)
        self.g_state_arm = 0

    #函数接口，外部接口
    #TODO 
    def arm_control_from_instuction(self,instruction):
        if self.g_state_arm == 0:
            closeTid = threading.Thread(target = self.ctrl_arm_move, args = [instruction])
            closeTid.setDaemon(True)
            closeTid.start()
            self.g_state_arm = 1
            
        if self.running == 1 and instruction == "Seven":
                self.running = 0

    
'''
Arm = Arm_Device()
time.sleep(.1)

look_at = [90, 164, 18, 0, 90, 90]
p_Prayer = [90, 90, 0, 180, 90, 180] 
p_Thumb_up = [90, 90, 90, 90, 90, 180] 
p_Heart_single = [90, 0, 180, 0, 90, 30] 
p_Eight = [90, 180, 18, 0, 90, 90] 
p_Congratulation = [90, 131, 52, 0, 90, 180] 
p_Rock = [90, 0, 90, 180, 90, 0] 
p_fist = [90, 90, 0, 0, 90, 0] 
p_horse_1 = [90, 7, 153, 19, 0, 126] 
p_horse_2 = [90, 5, 176, 0, 0, 180]
p_horse_3 = [90, 62, 158, 0, 0, 0]

# 定义移动机械臂函数,同时控制1-6号舵机运动，p=[S1,S2,S3,S4,S5,S6]
def arm_move_6(p, s_time = 500):
    for i in range(6):
        id = i + 1
        Arm.Arm_serial_servo_write(id, p[i], s_time)
        time.sleep(.01)
    time.sleep(s_time/1000)


global running
running = 0

# #蜂鸣器响起
# Arm.Arm_Buzzer_On(1)
# s_time = 300
# #直立
# arm_move_6(p_Thumb_up,s_time)
# time.sleep(1)

def clap(Arm, s_time):
    array_clap = [[90, 90, 90, 90, 90, 180],
                [90, 90, 90, 90, 90, 90]
                ]
    for index in range(3):
        arm_move_6(array_clap[0],s_time)
        time.sleep(0.3)
        arm_move_6(array_clap[1],s_time)
        time.sleep(0.3)
# Define hourse movment    
# 定义小马运动
def horse_running():
    Arm.Arm_serial_servo_write(6, 150, 300)
    time.sleep(.3)
    Arm.Arm_serial_servo_write(6, 180, 300)
    time.sleep(.3)

global g_state_arm
g_state_arm = 0
def ctrl_arm_move(index):
    global running
    if index == "Prayer":
        arm_move_6(p_Prayer, 1000)
        time.sleep(1.5)
        arm_move_6(look_at, 1000)
        time.sleep(1)
    elif index == "Thumb_up":
        s_time = 500
        Arm.Arm_serial_servo_write(6, 180, s_time)
        time.sleep(s_time/1000)
        Arm.Arm_serial_servo_write(6, 90, s_time)
        time.sleep(s_time/1000)
        Arm.Arm_serial_servo_write(6, 180, s_time)
        time.sleep(s_time/1000)
        Arm.Arm_serial_servo_write(6, 90, s_time)
        time.sleep(s_time/1000)
    elif index == "Ok":
        s_time = 300
        Arm.Arm_serial_servo_write(4, 10, s_time)
        time.sleep(s_time/1000)
        Arm.Arm_serial_servo_write(4, 0, s_time)
        time.sleep(s_time/1000)
        Arm.Arm_serial_servo_write(4, 10, s_time)
        time.sleep(s_time/1000)
        Arm.Arm_serial_servo_write(4, 0, s_time)
        time.sleep(s_time/1000)
    elif index == "Heart_single":
        arm_move_6([90, 90, 90, 90, 90, 90], 800)
        time.sleep(.1)
        arm_move_6(p_Heart_single, 1000)
        time.sleep(1)
    elif index == "Five":
        arm_move_6(look_at, 1000)
        time.sleep(.5)
    elif index == "Eight":
        s_time = 300
        arm_move_6(p_Eight, 0)
        time.sleep(1)
        Arm.Arm_serial_servo_write(2, 165, s_time)
        time.sleep(s_time/1000)
    elif index == "Rock":
        Arm.Arm_serial_servo_write6_array(p_Rock, 1300)
        time.sleep(3)
        Arm.Arm_serial_servo_write6_array(look_at, 1000)
        time.sleep(1)
    elif index == "Thumb_down": 
        Arm.Arm_serial_servo_write6_array(p_horse_1, 1300)
        time.sleep(1) 
    elif index == "Congratulation": 
        Arm.Arm_serial_servo_write6_array(p_horse_2, 1000)
        time.sleep(1)
        running = 1
        while running == 1:
            horse_running()
    elif index == "Seven": 
        Arm.Arm_Buzzer_On(8)   
        Arm.Arm_serial_servo_write6_array(p_horse_3, 1000)
        time.sleep(2)
        Arm.Arm_serial_servo_write6_array(look_at, 1000)
        time.sleep(1)
        

    global g_state_arm
    g_state_arm = 0
    
def start_move_arm(index):
   
    global g_state_arm
    global running
    if g_state_arm == 0:
        closeTid = threading.Thread(target = ctrl_arm_move, args = [index])
        closeTid.setDaemon(True)
        closeTid.start()
        g_state_arm = 1
        
    if running == 1 and index == "Seven":
            running = 0

try:
    Arm.Arm_Buzzer_On(1)
    s_time = 300
    Arm.Arm_serial_servo_write(4, 10, s_time)
    time.sleep(s_time/1000)
    Arm.Arm_serial_servo_write(4, 0, s_time)
    time.sleep(s_time/1000)
    Arm.Arm_serial_servo_write(4, 10, s_time)
    time.sleep(s_time/1000)
    Arm.Arm_serial_servo_write(4, 0, s_time)
    time.sleep(s_time/1000)
    
    while True:

        
        res = input("action:")
       
        if res == 'Prayer': 
            print('Recognition result：' + str(res))
           
            start_move_arm(res) 
        elif res == 'Thumb_up':
            print('Recognition result：' + str(res))
        
            start_move_arm(res)
        elif res == 'Ok': 
            print('Recognition result：' + str(res))
            start_move_arm(res)
        elif res == 'Heart_single': 
            print('Recognition result：' + str(res))
            start_move_arm(res)
        elif res == 'Five': 
            print('Recognition result：' + str(res))
            start_move_arm(res)
        elif res == "Eight": 
            print('Recognition result：' + str(res))
            start_move_arm(res)
            
        elif res == "Rock": 
            print('Recognition result：' + str(res))
            start_move_arm(res)
        elif res == "Congratulation": 
            print('Recognition result：' + str(res))
           
            start_move_arm(res)
        elif res == "Seven": 
            print('Recognition result：' + str(res))
           
            start_move_arm(res)
        elif res == "Thumb_down": 
            print('Recognition result：' + str(res))

            start_move_arm(res)    
        else:
            print("[arm control]Not define action!")

except KeyboardInterrupt:
    print(" Program closed! ")
    pass
'''