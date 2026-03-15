class DepthEstimator:
    def __init__(self, focal_length=800, real_height_cm=170):
        self.focal_length = focal_length
        self.real_height_cm = real_height_cm

    def estimate_distance(self, bbox_height_pixels):
        if not bbox_height_pixels or bbox_height_pixels <= 0: 
            return 0.0
            
        distance_cm = (self.focal_length * self.real_height_cm) / float(bbox_height_pixels)
        return round(distance_cm / 100.0, 2)