import cv2

class EnvironmentFixer:
    def __init__(self):
        pass

    def enhance_visibility(self, frame):
        # Khử sương mù cơ bản bằng cách tăng độ tương phản (CLAHE)
        lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        cl = clahe.apply(l)
        limg = cv2.merge((cl,a,b))
        enhanced_frame = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
        return enhanced_frame