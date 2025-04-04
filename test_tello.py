from djitellopy import Tello
import time

tello = Tello()

tello.connect()

print(f"Battery: {tello.get_battery()}%")

# Takeoff
tello.takeoff()

tello.move_up(30) 
   # move up 50 cm

tello.rotate_clockwise(180) # rotate 90 degrees
tello.flip_right()

# Land
time.sleep(2)
tello.land()



