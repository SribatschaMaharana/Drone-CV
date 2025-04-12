import cv2
from drone.tello_controller import TelloController
from drone.behaviour_controller import BehaviorController
from vision.yolo_detector import YOLODetector
from vision.color_tracking import ColorTracker
from utils.key_controls import KeyControls

def main():
    drone = TelloController()
    detector = YOLODetector()
    color_tracker = ColorTracker()
    behavior_controller = BehaviorController()
    keys = KeyControls()

    try:
        drone.connect()
        print("[INFO] Drone ready. Press 'u' (takeoff), 'd' (land), 'f' (follow), 'a' (avoid), 'n' (none), 't' (toggle tracking), 'q' (quit).")

        while True:
            try:
                frame = drone.get_frame()
                if frame is None:
                    print("[WARN] No frame received.")
                    continue

                annotated_frame = detector.detect(frame)
                tracked_frame, obj_center = color_tracker.detect(annotated_frame)

                key = cv2.waitKey(20) & 0xFF
                if keys.handle_keypress(key):
                    print("[INFO] Quit key pressed.")
                    break

                if keys.takeoff_triggered:
                    drone.takeoff()
                    keys.takeoff_triggered = False

                if keys.land_triggered:
                    drone.land()
                    keys.land_triggered = False

                behavior = keys.behavior
                action = None

                if keys.tracking_enabled:
                    action = behavior_controller.decide_action(obj_center, frame.shape, behavior)
                    print(f"[DEBUG] Behavior: {behavior}, Action: {action}, Object center: {obj_center}")

                    if action:
                        print(f"[DEBUG] Simulated action(s): {action}")
                        for act in action:
                            print(f"[DEBUG] Drone would move {act}.")
                    else:
                        print("[DEBUG] No action determined.")
                else:
                    print("[DEBUG] Tracking disabled.")

                cv2.imshow("Tello Tracking", tracked_frame)

            except Exception as e:
                print(f"[ERROR] Runtime error: {e}")
                break

    except KeyboardInterrupt:
        print("[INFO] Keyboard interrupt. Shutting down.")
    except Exception as e:
        print(f"[ERROR] Failed to start: {e}")
    finally:
        drone.cleanup()
        print("[INFO] Program ended.")

if __name__ == "__main__":
    main()
