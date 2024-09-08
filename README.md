# **工业大学 课程设计四
基于dof的机械臂目标检测项目，使用ROS作为通信框架，采集机械臂上的摄像头图像数据，并通过ROS消息sensor_msgs/Image 发布出来，同时采用YOLOv5 模型对手势动作进行识别，并返回识别结果，识别结果消息为 std_msgs/String，
机械臂节点订阅识别结果并做出对应的动作。

![项目逻辑框架](https://github.com/user-attachments/assets/57937d18-2de7-4448-bf81-b47b22ba10ab)


# 演示视频
[bilibili-课程设计四](https://www.bilibili.com/video/BV1Je411H7t4/?spm_id_from=333.999.0.0&vd_source=20ab5b37b7810aa07786f9a4d46b180a)

# 贡献
- 一位低调的朋友@[MJJ](https://github.com/2481366805)

