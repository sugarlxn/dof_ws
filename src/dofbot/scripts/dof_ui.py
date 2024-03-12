#!/usr/bin/env python3
#-*- coding:utf-8 -*-
import cv2

def on_trackbar(val):
    # 处理滑块数值变化事件
    print('Trackbar value: {}'.format(val))

def on_button(val):
    # 处理按钮点击事件
    print('Button clicked.')

def main():
    window_name = 'UI Window'
    img = cv2.imread('/home/lxn/YOLO/datasets/temp/tian.jpg')  # 读入图片

    cv2.namedWindow(window_name)
    cv2.imshow(window_name, img)

    # 创建滑块
    cv2.createTrackbar('Trackbar', window_name, 0, 100, on_trackbar)

    # 创建按钮
    cv2.createButton('Button', on_button, None, cv2.QT_PUSH_BUTTON, 0)

    # while True:
    #     cv2.imshow(window_name, img)
    #     key = cv2.waitKey(20) & 0xFF
    #     if key == ord('q'):
    #         break
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()