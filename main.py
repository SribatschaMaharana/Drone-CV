import cv2
from tello_controller import TelloController
from yolo_detector import YOLODetector

def main():
    drone = TelloController()
    detector = YOLODetector()

    try:
        drone.connect()
        print("start video stream. 'q' to quit.")

        while True:
            frame = drone.get_frame()
            labelled_frame = detector.detect(frame)

            cv2.imshow("Tello + YOLO Detection", labelled_frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except Exception as e:
        print(f"[ERROR] {e}")
    finally:
        drone.cleanup()

if __name__ == "__main__":
    main()
