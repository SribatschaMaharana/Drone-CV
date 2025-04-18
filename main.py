import time
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
        drone.takeoff()
        drone.drone.move_up(30)
        print("[INFO] Drone ready. Press 'f' (follow), 'a' (avoid), 'n' (none), 'q' to quit.")

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

                behavior = keys.behavior
                action = behavior_controller.decide_action(obj_center, frame.shape, behavior)

                print(f"[DEBUG] Behavior: {behavior}, Action: {action}, Object center: {obj_center}")


                if action:
                    print(f"[DEBUG] Executing actions: {action}")
                    for act in action:
                        if act == "forward":
                            drone.drone.move_forward(20)
                        elif act == "back":
                            drone.drone.move_back(20)
                        elif act == "left":
                            drone.drone.move_left(20)
                        elif act == "right":
                            drone.drone.move_right(20)
                        elif act == "up":
                            drone.drone.move_up(20)
                        elif act == "down":
                            drone.drone.move_down(20)
                        time.sleep(0.1)

                cv2.imshow("Tello Tracking", tracked_frame)

            except Exception as e:
                print(f"[ERROR] Runtime error: {e}")
                break

    except KeyboardInterrupt:
        print("[INFO] Keyboard interrupt. Shutting down.")
    except Exception as e:
        print(f"[ERROR] Failed to start: {e}")
    finally:
        drone.land()
        drone.cleanup()
        print("[INFO] Program ended.")

if __name__ == "__main__":
    main()
