import cv2
import numpy as np
from ultralytics import YOLO

# 1. Khai báo thẳng cấu hình vào code (Bỏ qua file YAML để né lỗi Windows)
config = {
    'camera': {'source': 0, 'width': 640, 'height': 480, 'fps': 30},
    'target': {'class_id': 0, 'confidence_threshold': 0.5},
    'gimbal': {'deadzone': 20}
}

# 2. Khởi tạo "Não" và "Mắt" (Mô hình YOLOv8 nano - siêu nhẹ)
print("[INFO] Đang tải mô hình YOLOv8n...")
model = YOLO("yolov8n.pt") 

# Khởi tạo Camera
cap = cv2.VideoCapture(config['camera']['source'])
cap.set(cv2.CAP_PROP_FRAME_WIDTH, config['camera']['width'])
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config['camera']['height'])

center_x_frame = config['camera']['width'] // 2
center_y_frame = config['camera']['height'] // 2
deadzone = config['gimbal']['deadzone']

print("[INFO] Bắt đầu luồng Video. Nhấn 'q' để thoát.")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # 3. Perception (Nhận thức): Phát hiện vật thể
    results = model.predict(frame, conf=config['target']['confidence_threshold'], verbose=False)
    
    target_found = False
    
    # Duyệt qua các kết quả nhận diện
    for box in results[0].boxes:
        cls_id = int(box.cls[0])
        if cls_id == config['target']['class_id']: # Nếu là 'person'
            target_found = True
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            
            # Tính toán tâm của mục tiêu
            cx_target = (x1 + x2) // 2
            cy_target = (y1 + y2) // 2
            
            # Vẽ bounding box và tâm mục tiêu
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.circle(frame, (cx_target, cy_target), 5, (0, 0, 255), -1)
            
            # 4. Control (Hành động): Tính toán sai số để điều khiển Gimbal
            error_x = cx_target - center_x_frame
            error_y = cy_target - center_y_frame
            
            pan_cmd = "DUNG"
            tilt_cmd = "DUNG"
            
            # Logic xoay trái/phải (Pan)
            if abs(error_x) > deadzone:
                pan_cmd = "XOAY PHAI ->" if error_x > 0 else "<- XOAY TRAI"
                
            # Logic xoay lên/xuống (Tilt)
            if abs(error_y) > deadzone:
                tilt_cmd = "CUI XUONG v" if error_y > 0 else "^ NGANG LEN"
                
            # Hiển thị lệnh Gimbal lên màn hình
            cv2.putText(frame, f"PAN: {pan_cmd}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)
            cv2.putText(frame, f"TILT: {tilt_cmd}", (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)
            
            # Chỉ bám theo mục tiêu đầu tiên tìm thấy
            break 
            
    if not target_found:
        cv2.putText(frame, "GIMBAL: TIM KIEM MUC TIEU...", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 165, 255), 2)

    # Vẽ tâm của khung hình (Crosshair)
    cv2.drawMarker(frame, (center_x_frame, center_y_frame), (0, 255, 255), cv2.MARKER_CROSS, 20, 2)

    # Hiển thị
    cv2.imshow("Gimbal CV Agent - DEMO", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()