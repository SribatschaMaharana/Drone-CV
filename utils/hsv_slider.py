import cv2
import numpy as np

def nothing(x):
    pass

# Open a video capture (set 0 for your built-in webcam, or use your Tello stream URL if available)
cap = cv2.VideoCapture(0)

# Create a window for the trackbars
cv2.namedWindow("Trackbars")

# Create trackbars for the lower HSV bound.
cv2.createTrackbar("Lower H", "Trackbars", 0, 179, nothing)
cv2.createTrackbar("Lower S", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("Lower V", "Trackbars", 0, 255, nothing)

# Create trackbars for the upper HSV bound.
cv2.createTrackbar("Upper H", "Trackbars", 179, 179, nothing)
cv2.createTrackbar("Upper S", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("Upper V", "Trackbars", 255, 255, nothing)

while True:
    ret, frame = cap.read()
    if not ret:
        print("[ERROR] Unable to capture video frame.")
        break

    # Convert frame to HSV color space.
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Get trackbar positions to define the HSV range.
    l_h = cv2.getTrackbarPos("Lower H", "Trackbars")
    l_s = cv2.getTrackbarPos("Lower S", "Trackbars")
    l_v = cv2.getTrackbarPos("Lower V", "Trackbars")
    u_h = cv2.getTrackbarPos("Upper H", "Trackbars")
    u_s = cv2.getTrackbarPos("Upper S", "Trackbars")
    u_v = cv2.getTrackbarPos("Upper V", "Trackbars")

    lower_hsv = np.array([l_h, l_s, l_v])
    upper_hsv = np.array([u_h, u_s, u_v])

    # Create a mask using the current HSV thresholds.
    mask = cv2.inRange(hsv, lower_hsv, upper_hsv)
    result = cv2.bitwise_and(frame, frame, mask=mask)

    # Display the original frame, the mask, and the result.
    cv2.imshow("Frame", frame)
    cv2.imshow("Mask", mask)
    cv2.imshow("Result", result)

    # Press 'q' to quit the tuner.
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
