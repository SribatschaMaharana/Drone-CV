from djitellopy import Tello
import cv2

#drone setup, connection, streaming, and control.
class TelloController:
    def __init__(self):
        self.drone = Tello()

    def connect(self):
        self.drone.connect()
        print(f"Battery level: {self.drone.get_battery()}%")
        self.drone.streamon()
        self.frame_reader = self.drone.get_frame_read()

    def get_frame(self):
        frame = self.frame_reader.frame
        return cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    def cleanup(self):
        self.drone.streamoff()
        cv2.destroyAllWindows()

    def takeoff(self):
        self.drone.takeoff()

    def land(self):
        self.drone.land()
