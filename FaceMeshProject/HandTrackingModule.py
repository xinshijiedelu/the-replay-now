import cv2
import mediapipe as mp
import time


class HandDetector:
    def __init__(self, mode=False, maxHands=2, detectionConf=0.5, trackingConf=0.5):
        # 初始化手部检测参数
        self.mode = mode  # 静态图像模式
        self.maxHands = maxHands  # 最大手部数量
        self.detectionConf = detectionConf  # 检测置信度
        self.trackingConf = trackingConf  # 跟踪置信度
        self.mpHands = mp.solutions.hands  # 导入 MediaPipe 手部解决方案

        # 创建手部检测器
        self.hands = self.mpHands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.maxHands,
            min_detection_confidence=self.detectionConf,
            min_tracking_confidence=self.trackingConf
        )
        self.mpDraw = mp.solutions.drawing_utils  # 用于绘制手部连接

    def findHands(self, img, draw=True):
        # 将图像从 BGR 转换为 RGB
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # 处理图像以检测手部
        self.results = self.hands.process(imgRGB)

        # 如果检测到手部，绘制连接
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms,
                                               self.mpHands.HAND_CONNECTIONS)
        return img  # 返回处理后的图像

    def findPosition(self, img, handNo=0, draw=True):
        # 获取手部关键点的位置
        lmList = []  # 存储关键点位置
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]  # 获取指定手部
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape  # 获取图像的高、宽和通道数
                cx, cy = int(lm.x * w), int(lm.y * h)  # 计算关键点的坐标
                lmList.append([id, cx, cy])  # 将坐标添加到列表
                if draw:
                    cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)  # 绘制关键点

        return lmList  # 返回关键点列表


def main():
    pTime = 0  # 上一帧时间
    cTime = 0  # 当前帧时间
    cap = cv2.VideoCapture(0)  # 打开摄像头

    if not cap.isOpened():
        print("无法打开摄像头。")
        return  # 如果摄像头无法打开，退出程序

    detector = HandDetector()  # 创建手部检测器实例

    while True:
        success, img = cap.read()  # 读取摄像头视频流
        if not success:
            print("无法读取摄像头视频流。")
            break  # 如果无法读取视频流，退出循环

        img = detector.findHands(img)  # 检测手部
        lmList = detector.findPosition(img)  # 获取手部关键点位置
        if lmList:
            print(lmList[4])  # 打印第5个关键点的位置（拇指尖）

        # 计算并显示帧率
        cTime = time.time()
        fps = 1 / (cTime - pTime) if (cTime - pTime) != 0 else 0
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                    (255, 0, 255), 3)  # 在图像上显示帧率

        cv2.imshow("Image", img)  # 显示图像

        # 退出条件
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break  # 按下 'q' 键退出循环

    cap.release()  # 释放摄像头
    cv2.destroyAllWindows()  # 关闭所有 OpenCV 窗口


if __name__ == "__main__":
    main()  # 运行主函数