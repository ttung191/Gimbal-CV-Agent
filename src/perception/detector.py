from ultralytics import YOLO

class Detector:
    """
    Module Nhận thức: Sử dụng AI để phát hiện và khoanh vùng mục tiêu.
    """
    def __init__(self, model_path="models/detection/yolov8n.pt", conf_thresh=0.5, target_class=0):
        print(f"[INFO] Dang tai mo hinh nhan dien: {model_path}")
        self.model = YOLO(model_path)
        self.conf_thresh = conf_thresh
        self.target_class = target_class

    def detect(self, frame):
        """
        Phân tích khung hình và trả về thông tin mục tiêu (nếu có)
        """
        results = self.model.predict(frame, conf=self.conf_thresh, verbose=False)
        target_info = None

        for box in results[0].boxes:
            cls_id = int(box.cls[0])
            if cls_id == self.target_class:
                # Lấy tọa độ bounding box
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                
                # Tính tâm mục tiêu
                cx = (x1 + x2) // 2
                cy = (y1 + y2) // 2
                
                target_info = {
                    "bbox": (x1, y1, x2, y2),
                    "center": (cx, cy)
                }
                break # Chỉ lấy mục tiêu đầu tiên tìm thấy để tránh nhiễu
                
        return target_info