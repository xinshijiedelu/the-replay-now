import time
import cv2
import mediapipe as mp

# 初始化 Mediapipe Hands 模块
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# 初始化 Mediapipe 绘制模块
mp_drawing = mp.solutions.drawing_utils
pTime = 0  # 前一帧时间
cTime = 0  # 当前帧时间

# 打开摄像头
cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    if not success:
        print("无法读取摄像头视频流。")
        break

    # 将 BGR 图像转换为 RGB 图像
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # 处理图像
    results = hands.process(imgRGB)

    # 绘制手部关键点
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            for id, lm in enumerate(hand_landmarks.landmark):
                # 打印每个关键点的 ID 和位置
                #print(id, lm)
                h,w,c = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                print(id,cx,cy)
                if id==4:
                    cv2.circle(img,(cx,cy),25,(255,0,255),cv2.FILLED)
            # 绘制手部关键点及其连接
            mp_drawing.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # 计算 FPS
    cTime = time.time()
    fps = 1 / (cTime - pTime) if (cTime - pTime) != 0 else 0
    pTime = cTime

    # 显示 FPS
    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

    # 显示图像
    cv2.imshow("Image", img)

    # 退出条件
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 释放资源
cap.release()
cv2.destroyAllWindows()