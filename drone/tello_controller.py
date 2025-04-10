from djitellopy import Tello
import cv2

#drone setup, connection, streaming, and control.
class TelloController:
    def __init__(self):
        self.drone = Tello()

    def connect(self):
        self.drone.connect()
        print(f"Battery level: {self.drone.get_battery()}%")
        print("[DEBUG] Starting video stream...")
        self.drone.streamon()
        print("[DEBUG] Stream started.")

        self.frame_reader = self.drone.get_frame_read()

    def get_frame(self):
        frame = self.frame_reader.frame
        if frame is None:
            print("[WARN] No frame received from drone.")
            return None
        return cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    def cleanup(self):
        try:
            if self.drone.stream_on:
                self.drone.streamoff()
        except Exception as e:
            print(f"[WARN] Failed to stop stream: {e}")
        try:
            cv2.destroyAllWindows()
        except Exception as e:
            print(f"[WARN] Failed to close OpenCV windows: {e}")


    def takeoff(self):
        self.drone.takeoff()

    def land(self):
        self.drone.land()
