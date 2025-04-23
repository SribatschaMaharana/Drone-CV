import time
from djitellopy import Tello
from pynput import keyboard

drone = Tello()
speed = 50
rc_values = {"lr": 0, "fb": 0, "ud": 0, "yaw": 0}
flying = False

def update_rc():
    drone.send_rc_control(rc_values["lr"], rc_values["fb"], rc_values["ud"], rc_values["yaw"])

def on_press(key):
    global flying
    try:
        k = key.char.lower()
        if k == 'w':
            rc_values["fb"] = speed
        elif k == 's':
            rc_values["fb"] = -speed
        elif k == 'a':
            rc_values["lr"] = -speed
        elif k == 'd':
            rc_values["lr"] = speed
        elif k == 'r':
            rc_values["ud"] = speed
        elif k == 'f':
            rc_values["ud"] = -speed
        elif k == 'q':
            rc_values["yaw"] = -speed
        elif k == 'e':
            rc_values["yaw"] = speed
        elif k == 't' and not flying:
            drone.takeoff()
            flying = True
        elif k == 'n' and flying:
            drone.land()
            flying = False
        update_rc()
    except:
        pass

def on_release(key):
    try:
        k = key.char.lower()
        if k in ['w', 's']:
            rc_values["fb"] = 0
        elif k in ['a', 'd']:
            rc_values["lr"] = 0
        elif k in ['r', 'f']:
            rc_values["ud"] = 0
        elif k in ['q', 'e']:
            rc_values["yaw"] = 0
        update_rc()
    except:
        if key == keyboard.Key.esc:
            print("[INFO] ESC pressed. Landing + quitting.")
            if flying:
                drone.land()
            drone.streamoff()
            return False  # stop

def main():
    drone.connect()
    drone.streamon()
    print("[INFO] Drone connected. Press T to takeoff, N to land. Use WASD+RF+QE. ESC to quit.")

    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

if __name__ == "__main__":
    main()
