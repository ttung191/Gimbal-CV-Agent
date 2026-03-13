import queue

class FrameBuffer:
    def __init__(self, max_size=10):
        self.q = queue.Queue(maxsize=max_size)
        # Quản lý hàng đợi frame để luồng đọc camera và luồng AI không chờ nhau gây nghẽn