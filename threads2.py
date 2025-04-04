import cv2
import threading
import time
from djitellopy import Tello

def perform_tello_movements(drone: Tello):
    """
    Performs a sequence of movements while streaming is active.
    """
    print(f"Battery: {drone.get_battery()}%")

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

    while True:
        frame = frame_read.frame  # Get current frame
        cv2.imshow("Tello Stream", frame)  # Show the frame in a window

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()
    drone.streamoff()

def main():
    # Initialize Tello drone
    tello = Tello()
    tello.connect()

    # Start the movement thread
    movement_thread = threading.Thread(target=perform_tello_movements, args=(tello,))
    movement_thread.start()

    # Run the video stream in the main thread
    stream_tello_video(tello)

    # Wait for the movement thread to finish
    movement_thread.join()

if __name__ == "__main__":
    main()
