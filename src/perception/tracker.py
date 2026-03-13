class ObjectTracker:
    def __init__(self):
        # Tương lai sẽ tích hợp DeepSORT hoặc ByteTrack ở đây
        self.track_id_counter = 0

    def update(self, detections, frame):
        # Gắn ID cho vật thể để Gimbal không bị nhầm lẫn khi có 2 người đứng cạnh nhau
        tracked_objects = []
        for det in detections:
            self.track_id_counter += 1
            det['track_id'] = self.track_id_counter
            tracked_objects.append(det)
        return tracked_objects