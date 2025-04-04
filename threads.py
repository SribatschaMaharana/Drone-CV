import cv2
import threading
import time
from djitellopy import Tello

def perform_tello_movements(drone: Tello):
    """
    Performs movements while the video stream is active.
    """
    time.sleep(3)  

    print(f"Battery: {drone.get_battery()}%")


    drone.send_command_with_return("motoron")
    time.sleep(1)

    drone.takeoff()
    time.sleep(2)

    drone.move_up(30)  # Move up 30 cm
    time.sleep(1)

    drone.rotate_clockwise(180)  # Rotate 180 degrees
    time.sleep(1)

    drone.flip_right()  # Flip right
    time.sleep(1)

    drone.land()  # Land the drone
    print("Landing...")

def stream_tello_video(drone: Tello):
    """
    Streams video from the Tello drone to the laptop in real-time.
    Press 'q' to exit the stream.
    """
    drone.streamon()

    frame_read = drone.get_frame_read()

    time.sleep(2)  # Give time for the stream to start

    while True:
        frame = frame_read.frame
        if frame is None or frame.size == 0:
            print("⚠️ Warning: Empty frame received!")
            continue

        cv2.imshow("Tello Stream", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()
    drone.streamoff()

def main():
    tello = Tello()
    tello.connect()

    movement_thread = threading.Thread(target=perform_tello_movements, args=(tello,))
    movement_thread.start()

    stream_tello_video(tello)

    movement_thread.join()

if __name__ == "__main__":
    main()
