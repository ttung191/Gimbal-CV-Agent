from collections import deque

class ShortTermMemory:
    def __init__(self, max_size=30):
        self.history = deque(maxlen=max_size) # Lưu tối đa 30 frame gần nhất

    def remember(self, target_center):
        if target_center:
            self.history.append(target_center)

    def get_last_known_position(self):
        if len(self.history) > 0:
            return self.history[-1]
        return None