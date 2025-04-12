import cv2

class KeyControls:
    def __init__(self):
        self.behavior = None
    
    def get_behavior(self):
        return self.behavior

    def handle_keypress(self, key):
        if key == ord('f'):
            print("[KEY] Set behavior: follow")
            self.behavior = "follow"
        elif key == ord('a'):
            print("[KEY] Set behavior: avoid")
            self.behavior = "avoid"
        elif key == ord('t'):
            print("[KEY] Set behavior: track")
            self.behavior = "track"
        elif key == ord('n'):
            print("[KEY] Set behavior: none")
            self.behavior = None

        return key == ord('q')  # Quit signal
