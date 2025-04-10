import cv2
from drone.tello_controller import TelloController
from vision.yolo_detector import YOLODetector

def main():
    drone = TelloController()
    detector = YOLODetector()

    try:
        drone.connect()
        print("start video stream. 'q' to quit.")

        while True:
            try:
                frame = drone.get_frame()

                if frame is None:
                    print("[WARN] No frame received.")
                    continue

                annotated = detector.detect(frame)
                cv2.imshow("Tello + YOLO Detection", annotated)

                # Use a slightly longer delay to help with GUI rendering on Mac
                key = cv2.waitKey(20) & 0xFF
                if key == ord('q'):
                    print("[INFO] 'q' pressed. Exiting.")
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
