from djitellopy import Tello
import time

tello = Tello()

tello.connect()

print(f"Battery: {tello.get_battery()}%")

# Takeoff
tello.takeoff()

tello.move_up(50)  # move up 50 cm
tello.move_forward(100)  # move forward 100 cm

tello.rotate_clockwise(90) # rotate 90 degrees
tello.move_forward(50)  # move forward another 50 cm

# Land
time.sleep(2)
tello.land()

tello.end()

