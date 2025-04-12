class BehaviorController:
    def __init__(self, frame_width=960):
        self.frame_center_x = frame_width // 2
        self.threshold = 50  # pixels

    def decide_action(self, object_center, frame_shape, behavior):
        if object_center is None or behavior is None:
            return None

        frame_h, frame_w = frame_shape[:2]
        cx, cy = object_center
        offset_x = cx - (frame_w // 2)
        offset_y = cy - (frame_h // 2)

        commands = []

        if abs(offset_x) > self.threshold:
            if offset_x > 0:
                commands.append("right" if behavior == "follow" else "left")
            else:
                commands.append("left" if behavior == "follow" else "right")

        if abs(offset_y) > self.threshold:
            if offset_y > 0:
                commands.append("down" if behavior == "follow" else "up")
            else:
                commands.append("up" if behavior == "follow" else "down")

        if not commands:
            commands.append("forward" if behavior == "follow" else "back")

        return commands

