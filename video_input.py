import cv2
from djitellopy import tello

def stream_tello_video():
    """
    Streams video from the Tello drone to the laptop in real-time.
    Press 'q' to exit the stream.
    """
    # Initialize Tello drone and connect
    drone = tello.Tello()
    drone.connect()
    drone.streamon()

    # Get video stream reader
    frame_read = drone.get_frame_read()

    try:
        while True:
            frame = frame_read.frame  # Get current frame
            img = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            cv2.imshow("Tello Stream", img)  # Show the frame in a window

            # Press 'q' to exit the video stream
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    except Exception as e:
        print(f"Error in streaming: {e}")
    finally:
        cv2.destroyAllWindows()
        drone.streamoff()  # Turn off streaming

if __name__ == "__main__":
    stream_tello_video()
