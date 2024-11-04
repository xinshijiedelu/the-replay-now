import cv2  # OpenCV库，用于视频处理和图像操作
import time  # 用于计算帧率（FPS）
import numpy as np  # 数值计算库，用于音量插值
import HandTrackingModule as htm  # 自定义模块，用于手部跟踪
import math  # 数学函数库，用于计算距离
from ctypes import cast, POINTER  # 用于处理音频接口
from comtypes import CLSCTX_ALL  # 用于音频接口的上下文
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume  # pycaw库用于音量控制

# 设置摄像头参数
wCam, hCam = 640, 480  # 摄像头分辨率

# 初始化摄像头
cap = cv2.VideoCapture(0)  # 尝试使用默认摄像头
cap.set(3, wCam)  # 设置摄像头宽度
cap.set(4, hCam)  # 设置摄像头高度
pTime = 0  # 上一帧时间，用于计算FPS

# 初始化手部检测器
detector = htm.HandDetector()  # 创建手部检测器对象

# 初始化系统音频控制
devices = AudioUtilities.GetSpeakers()  # 获取系统音频设备
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)  # 激活音量接口
volume = cast(interface, POINTER(IAudioEndpointVolume))  # 将接口转换为音量控制指针
volRange = volume.GetVolumeRange()  # 获取音量范围
minVol = volRange[0]  # 最小音量
maxVol = volRange[1]  # 最大音量
vol = 0  # 当前音量
volBar = 400  # 音量条高度
volPer = 0  # 音量百分比

while True:
    success, img = cap.read()  # 读取摄像头图像
    img = detector.findHands(img)  # 在图像中查找手部
    lmList = detector.findPosition(img, draw=False)  # 获取手部关键点位置
    if len(lmList) != 0:  # 如果检测到手部
        # 获取两个关键点的位置（可能是手指末端）
        x1, y1 = lmList[4][1], lmList[4][2]  # 拇指末端
        x2, y2 = lmList[8][1], lmList[8][2]  # 食指末端
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2  # 计算中点位置

        # 绘制关键点和连线
        cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)  # 绘制拇指末端
        cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)  # 绘制食指末端
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)  # 连接拇指和食指
        cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)  # 绘制中点

        length = math.hypot(x2 - x1, y2 - y1)  # 计算手指间距离

        # 根据距离调整音量
        vol = np.interp(length, [50, 300], [minVol, maxVol])  # 插值计算当前音量
        volBar = np.interp(length, [50, 300], [400, 150])  # 插值计算音量条高度
        volPer = np.interp(length, [50, 300], [0, 100])  # 插值计算音量百分比
        print(int(length), vol)  # 打印距离和音量值
        volume.SetMasterVolumeLevel(vol, None)  # 设置系统音量

        if length < 50:  # 如果手指距离小于50，则显示绿色圆圈
            cv2.circle(img, (cx, cy), 15, (0, 255, 0), cv2.FILLED)

    # 绘制音量条和百分比
    cv2.rectangle(img, (50, 150), (85, 400), (255, 0, 0), 3)  # 绘制音量条边框
    cv2.rectangle(img, (50, int(volBar)), (85, 400), (255, 0, 0), cv2.FILLED)  # 绘制音量条填充
    cv2.putText(img, f'{int(volPer)} %', (40, 450), cv2.FONT_HERSHEY_COMPLEX,
                1, (255, 0, 0), 3)  # 显示音量百分比

    # 计算并显示FPS
    cTime = time.time()  # 当前时间
    fps = 1 / (cTime - pTime)  # 计算FPS
    pTime = cTime  # 更新上一帧时间
    cv2.putText(img, f'FPS: {int(fps)}', (40, 50), cv2.FONT_HERSHEY_COMPLEX,
                1, (255, 0, 0), 3)  # 显示FPS

    cv2.imshow("Img", img)  # 显示处理后的图像

    # 检查按键输入
    key = cv2.waitKey(1)  # 等待1毫秒以检测按键
    if key == ord('q'):  # 如果按下 'q' 键
        break  # 退出循环

# 释放资源
cap.release()  # 释放摄像头资源
cv2.destroyAllWindows()  # 关闭所有OpenCV窗口