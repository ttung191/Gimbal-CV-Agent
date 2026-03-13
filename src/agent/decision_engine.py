class DecisionEngine:
    def __init__(self, memory_module):
        self.memory = memory_module

    def evaluate(self, current_target):
        if current_target is None:
            last_pos = self.memory.get_last_known_position()
            if last_pos:
                return "Target lost! Predicting from memory..."
            return "Idle. Searching for target..."
        
        self.memory.remember(current_target)
        return "Target locked. Tracking!"