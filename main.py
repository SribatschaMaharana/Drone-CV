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
            try:
                frame = drone.get_frame()
                annotated = detector.detect(frame)
                cv2.imshow("Tello + YOLO Detection", annotated)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            except Exception as e:
                print(f"[ERROR] Frame read or detection failed: {e}")
                break

    except KeyboardInterrupt:
        print("\n[INFO] Keyboard interrupt received. Shutting down.")
    except Exception as e:
        print(f"[ERROR] Failed to start drone or video stream: {e}")
    finally:
        try:
            drone.cleanup()
        except Exception as e:
            print(f"[WARN] Cleanup skipped due to error: {e}")
        print("[INFO] Program ended.")

if __name__ == "__main__":
    main()
