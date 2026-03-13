import cv2

class StreamReader:
    """
    Module chịu trách nhiệm kết nối và đọc luồng video từ Camera/Gimbal.
    """
    def __init__(self, source=0, width=640, height=480):
        self.source = source
        self.width = width
        self.height = height
        self.cap = None

    def start(self):
        """Mở kết nối tới camera"""
        print(f"[INFO] Dang khoi tao luong video tu nguon: {self.source}")
        self.cap = cv2.VideoCapture(self.source)
        
        # Thiết lập độ phân giải
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        
        if not self.cap.isOpened():
            raise ValueError(f"[ERROR] Khong the mo camera nguon {self.source}. Vui long kiem tra lai ket noi.")
        return self

    def read_frame(self):
        """Đọc một khung hình từ camera"""
        if self.cap is None or not self.cap.isOpened():
            return False, None
        return self.cap.read()

    def stop(self):
        """Giải phóng tài nguyên khi kết thúc"""
        if self.cap:
            self.cap.release()
            print("[INFO] Da dong luong video.")