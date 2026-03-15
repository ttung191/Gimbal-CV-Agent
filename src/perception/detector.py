from ultralytics import YOLO

class Detector:
    def __init__(self, model_path="yolo11n.onnx", conf_thresh=0.5, target_class=0):
        self.model = YOLO(model_path, task='detect')
        self.conf_thresh = conf_thresh
        self.target_class = target_class

    def detect_and_track(self, frame):
        results = self.model.track(frame, conf=self.conf_thresh, persist=True, tracker="bytetrack.yaml", verbose=False)
        target_info = None

        if results[0].boxes.id is not None:
            boxes = results[0].boxes
            for i in range(len(boxes)):
                cls_id = int(boxes.cls[i])
                if cls_id == self.target_class:
                    x1, y1, x2, y2 = map(int, boxes.xyxy[i])
                    track_id = int(boxes.id[i])
                    
                    cx = (x1 + x2) // 2
                    cy = (y1 + y2) // 2
                    
                    target_info = {
                        "track_id": track_id,
                        "bbox": (x1, y1, x2, y2),
                        "center": (cx, cy),
                        "height": y2 - y1
                    }
                    break 
                
        return target_info