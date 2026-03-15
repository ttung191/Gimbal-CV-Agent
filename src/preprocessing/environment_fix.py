import cv2

class EnvironmentFixer:
    def __init__(self, clip_limit=2.0, tile_size=(8, 8)):
        self.clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_size)

    def enhance_visibility(self, frame):
        yuv = cv2.cvtColor(frame, cv2.COLOR_BGR2YUV)
        yuv[:,:,0] = self.clahe.apply(yuv[:,:,0])
        enhanced_frame = cv2.cvtColor(yuv, cv2.COLOR_YUV2BGR)
        return enhanced_frame