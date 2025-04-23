import time
import cv2
from drone.tello_controller import TelloController
from vision.color_tracking import ColorTracker

def main():
    drone = TelloController()
    color_tracker = ColorTracker()

    try:
        drone.connect()
        drone.takeoff()
        drone.drone.move_up(30)
        print("[INFO] RC Control mode. Ctrl+C to land.")

        while True:
            frame = drone.get_frame()
            if frame is None:
                continue

            # get color, enter + radius
            tracked_frame, center = color_tracker.detect(frame)
            print(f"[DEBUG] Center: {center}, Radius: {color_tracker.last_radius}")
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            mask1 = cv2.inRange(hsv, color_tracker.lower_red1, color_tracker.upper_red1)
            mask2 = cv2.inRange(hsv, color_tracker.lower_red2, color_tracker.upper_red2)
            mask = cv2.bitwise_or(mask1, mask2)
            cv2.imshow("Debug Mask", mask)
            radius = color_tracker.last_radius

            lr = fb = ud = yaw = 0
            frame_h, frame_w = frame.shape[:2]

            if center:
                cx, cy = center
                offset_x = cx - (frame_w // 2)
                offset_y = cy - (frame_h // 2)

                # rotate on x offset
                if abs(offset_x) > 50:
                    yaw = int(offset_x / 10)

                # height on y offset
                if abs(offset_y) > 50:
                    ud = -20 if offset_y > 0 else 20

                # horizontal on size
                if radius:
                    target_radius = 50  # Tune this for ~2ft distance
                    if abs(radius - target_radius) > 10:
                        fb = 20 if radius < target_radius else -20

            # RC
            drone.send_rc(lr, fb, ud, yaw)

            cv2.imshow("RC Tracking", tracked_frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            time.sleep(0.05)  # throttle rc command

    except KeyboardInterrupt:
        print("[INFO] Interrupted. Landing.")
    finally:
        drone.land()
        drone.cleanup()
        print("[INFO] Shutdown complete.")

if __name__ == "__main__":
    main()
