import logging

class AgentLogger:
    def __init__(self, name="GimbalAgent"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        # Format log: [Thời gian] - [Mức độ] - [Nội dung]
        formatter = logging.Formatter('[%(asctime)s] - [%(levelname)s] - %(message)s', datefmt='%H:%M:%S')
        
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

    def info(self, msg): self.logger.info(msg)
    def warning(self, msg): self.logger.warning(msg)
    def error(self, msg): self.logger.error(msg)