class GimbalController:
    def __init__(self, frame_width, frame_height, deadzone=20, alpha=0.4):
        self.center_x = frame_width // 2
        self.center_y = frame_height // 2
        self.deadzone = deadzone
        self.alpha = alpha
        self.smoothed_x = None
        self.smoothed_y = None

    def apply_low_pass_filter(self, current_x, current_y):
        if self.smoothed_x is None or self.smoothed_y is None:
            self.smoothed_x, self.smoothed_y = current_x, current_y
            return current_x, current_y
        
        self.smoothed_x = (self.alpha * current_x) + ((1 - self.alpha) * self.smoothed_x)
        self.smoothed_y = (self.alpha * current_y) + ((1 - self.alpha) * self.smoothed_y)
        
        return int(self.smoothed_x), int(self.smoothed_y)

    def calculate_commands(self, target_center):
        if target_center is None:
            self.smoothed_x = None
            self.smoothed_y = None
            return "STOP", "STOP", 0, 0

        cx, cy = target_center
        smooth_cx, smooth_cy = self.apply_low_pass_filter(cx, cy)

        error_x = smooth_cx - self.center_x
        error_y = smooth_cy - self.center_y

        pan_cmd = "STOP"
        tilt_cmd = "STOP"

        if abs(error_x) > self.deadzone:
            pan_cmd = "PAN RIGHT ->" if error_x > 0 else "<- PAN LEFT"

        if abs(error_y) > self.deadzone:
            tilt_cmd = "TILT DOWN v" if error_y > 0 else "^ TILT UP"

        return pan_cmd, tilt_cmd, error_x, error_y