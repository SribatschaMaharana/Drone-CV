import cv2
import numpy as np
from djitellopy import Tello

def nothing(x):
    pass

def main():
    tello = Tello()
    tello.connect()
    print(f"[INFO] Battery: {tello.get_battery()}%")

    tello.streamon()
    frame_read = tello.get_frame_read()


    cv2.namedWindow("Trackbars")

    cv2.createTrackbar("Lower H", "Trackbars", 0, 179, nothing)
    cv2.createTrackbar("Lower S", "Trackbars", 0, 255, nothing)
    cv2.createTrackbar("Lower V", "Trackbars", 0, 255, nothing)

    cv2.createTrackbar("Upper H", "Trackbars", 179, 179, nothing)
    cv2.createTrackbar("Upper S", "Trackbars", 255, 255, nothing)
    cv2.createTrackbar("Upper V", "Trackbars", 255, 255, nothing)

    print("[INFO] Press 'q' to quit")

    while True:
        frame = frame_read.frame
        frame = cv2.convertScaleAbs(frame, alpha=1.2, beta=20)  #  brightness/contrast
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)          # color space

        frame = cv2.resize(frame, (640, 480))
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        l_h = cv2.getTrackbarPos("Lower H", "Trackbars")
        l_s = cv2.getTrackbarPos("Lower S", "Trackbars")
        l_v = cv2.getTrackbarPos("Lower V", "Trackbars")
        u_h = cv2.getTrackbarPos("Upper H", "Trackbars")
        u_s = cv2.getTrackbarPos("Upper S", "Trackbars")
        u_v = cv2.getTrackbarPos("Upper V", "Trackbars")

        lower_hsv = np.array([l_h, l_s, l_v])
        upper_hsv = np.array([u_h, u_s, u_v])

        mask = cv2.inRange(hsv, lower_hsv, upper_hsv)
        result = cv2.bitwise_and(frame, frame, mask=mask)

        cv2.imshow("Tello Camera", frame)
        cv2.imshow("Mask", mask)
        cv2.imshow("Filtered Result", result)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

    tello.streamoff()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
