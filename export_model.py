from ultralytics import YOLO

print("[INFO] Đang tải mô hình YOLO11 Nano thế hệ mới...")
model = YOLO("yolo11n.pt") 

print("[INFO] Đang tối ưu hóa và chuyển đổi sang định dạng ONNX...")
model.export(format="onnx", dynamic=True)

print("[SUCCESS] Đã xuất file yolo11n.onnx thành công! Sẵn sàng tích hợp.")