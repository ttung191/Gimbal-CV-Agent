class GimbalController:
    """
    Action Module: Calculate errors and issue PTZ (Pan-Tilt-Zoom) commands.
    """
    def __init__(self, frame_width, frame_height, deadzone=20):
        self.center_x = frame_width // 2
        self.center_y = frame_height // 2
        self.deadzone = deadzone

    def calculate_commands(self, target_center):
        if target_center is None:
            return "STOP", "STOP", 0, 0

        cx, cy = target_center
        error_x = cx - self.center_x
        error_y = cy - self.center_y

        pan_cmd = "STOP"
        tilt_cmd = "STOP"

        # Pan Logic (Left/Right)
        if abs(error_x) > self.deadzone:
            pan_cmd = "PAN RIGHT ->" if error_x > 0 else "<- PAN LEFT"

        # Tilt Logic (Up/Down)
        if abs(error_y) > self.deadzone:
            tilt_cmd = "TILT DOWN v" if error_y > 0 else "^ TILT UP"

        return pan_cmd, tilt_cmd, error_x, error_y