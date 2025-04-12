import cv2
import numpy as np

class ColorTracker:
    def __init__(self, lower_hsv=(51,54,39), upper_hsv=(140,206, 225)):

        self.lower_hsv = np.array(lower_hsv)
        self.upper_hsv = np.array(upper_hsv)

    def detect(self, frame):
        blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, self.lower_hsv, self.upper_hsv)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        contours, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        center = None

        if contours:
            largest = max(contours, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(largest)

            if radius > 10:
                center = (int(x), int(y))
                cv2.circle(frame, center, int(radius), (0, 255, 255), 2)

        return frame, center
