import cv2
import threading
import queue
import time

class StreamReader:
    """
    Module đọc luồng video được tối ưu hóa bằng Đa luồng (Multi-threading).
    Giúp tránh nghẽn cổ chai (I/O Bottleneck) cho bộ phận AI.
    """
    def __init__(self, source=0, width=640, height=480, queue_size=5):
        self.source = source
        self.width = width
        self.height = height
        self.cap = None
        # Hàng đợi frame lưu trữ tối đa queue_size frame
        self.q = queue.Queue(maxsize=queue_size)
        self.stopped = False

    def start(self):
        print(f"[INFO] Khởi tạo luồng video từ nguồn: {self.source}")
        self.cap = cv2.VideoCapture(self.source)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        
        if not self.cap.isOpened():
            raise ValueError(f"[ERROR] Không thể mở camera {self.source}.")
        
        # Bật một luồng (thread) chạy ngầm chỉ để đọc frame liên tục
        t = threading.Thread(target=self._update, args=())
        t.daemon = True
        t.start()
        return self

    def _update(self):
        """Hàm chạy ngầm liên tục đẩy frame mới vào hàng đợi."""
        while not self.stopped:
            if not self.q.full():
                ret, frame = self.cap.read()
                if not ret:
                    self.stop()
                    return
                self.q.put(frame)
            else:
                time.sleep(0.01) # Nghỉ nhẹ nếu hàng đợi đã đầy để nhường CPU

    def read_frame(self):
        """Lấy frame mới nhất từ hàng đợi."""
        if self.q.empty():
            return False, None
        return True, self.q.get()

    def stop(self):
        self.stopped = True
        if self.cap:
            self.cap.release()
        print("[INFO] Đã đóng luồng video.")