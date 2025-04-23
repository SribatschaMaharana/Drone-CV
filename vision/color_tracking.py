import cv2
import numpy as np

class ColorTracker:
    def __init__(self):
        # Lower red range (0–10)
        self.lower_red1 = np.array([0, 50, 50])
        self.upper_red1 = np.array([10, 255, 255])

        # Upper red range (160–179)
        self.lower_red2 = np.array([160, 50, 50])
        self.upper_red2 = np.array([179, 255, 255])

        self.last_radius = None

    def detect(self, frame):
        blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

        # dual mask
        mask1 = cv2.inRange(hsv, self.lower_red1, self.upper_red1)
        mask2 = cv2.inRange(hsv, self.lower_red2, self.upper_red2)
        mask = cv2.bitwise_or(mask1, mask2)

        # clean up 
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        contours, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        center = None
        self.last_radius = None

        if contours:
            largest = max(contours, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(largest)

            if radius > 10:
                center = (int(x), int(y))
                self.last_radius = radius
                cv2.circle(frame, center, int(radius), (0, 255, 255), 2)

        # Debug overlay
        cv2.putText(frame, f"Radius: {int(self.last_radius) if self.last_radius else 0}",
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        cv2.circle(frame, (frame.shape[1]//2, frame.shape[0]//2), 5, (255, 255, 255), -1)

        return frame, center
