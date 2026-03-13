class DepthEstimator:
    def __init__(self, focal_length=800, real_height_cm=170):
        self.focal_length = focal_length
        self.real_height_cm = real_height_cm # Chiều cao trung bình của người

    def estimate_distance(self, bbox_height_pixels):
        # Dùng công thức quang học cơ bản: Khoảng cách = (Tiêu cự * Chiều cao thực) / Chiều cao trên ảnh
        if bbox_height_pixels <= 0: return 0
        distance_cm = (self.focal_length * self.real_height_cm) / bbox_height_pixels
        return round(distance_cm / 100, 2) # Trả về đơn vị mét