import cv2
import time

from src.core.logger import AgentLogger
from src.core.metrics import FPSCounter
from src.ingestion.stream_reader import StreamReader
from src.perception.detector import Detector
from src.perception.depth_estimator import DepthEstimator
from src.preprocessing.environment_fix import EnvironmentFixer
from src.agent.memory import ShortTermMemory
from src.agent.decision_engine import DecisionEngine
from src.control.gimbal_controller import GimbalController

def main():
    logger = AgentLogger(name="MainApp")
    logger.info("Đang khởi động hệ thống Gimbal CV Agent (YOLO11 - ONNX)...")

    frame_width, frame_height = 640, 480
    
    try:
        streamer = StreamReader(source=0, width=frame_width, height=frame_height).start()
    except Exception as e:
        logger.error(f"Lỗi khởi tạo luồng video: {e}")
        return

    env_fixer = EnvironmentFixer()
    
    # Sử dụng mô hình ONNX siêu tốc
    detector = Detector(model_path="yolo11n.onnx", conf_thresh=0.5, target_class=0)
    depth_estimator = DepthEstimator()
    
    memory = ShortTermMemory(max_size=30)
    decision_engine = DecisionEngine(memory_module=memory)
    gimbal_ctrl = GimbalController(frame_width=frame_width, frame_height=frame_height, deadzone=30, alpha=0.4)
    fps_counter = FPSCounter()

    logger.info("Hệ thống đã sẵn sàng. Bắt đầu vòng lặp chính.")

    while True:
        ret, frame = streamer.read_frame()
        if not ret or frame is None:
            continue 

        fps = fps_counter.update()

        # Bỏ comment dòng dưới nếu muốn bật khử sương mù/thiếu sáng
        # frame = env_fixer.enhance_visibility(frame)

        target_info = detector.detect_and_track(frame)
        target_center = target_info["center"] if target_info else None

        agent_status = decision_engine.evaluate(target_center)
        
        active_target_pos = target_center 
        if not active_target_pos and "Predicting" in agent_status:
            active_target_pos = memory.get_last_known_position()

        pan_cmd, tilt_cmd, err_x, err_y = gimbal_ctrl.calculate_commands(active_target_pos)

        # Vẽ HUD
        cv2.line(frame, (frame_width//2 - 20, frame_height//2), (frame_width//2 + 20, frame_height//2), (0, 255, 0), 2)
        cv2.line(frame, (frame_width//2, frame_height//2 - 20), (frame_width//2, frame_height//2 + 20), (0, 255, 0), 2)

        if target_info:
            x1, y1, x2, y2 = target_info["bbox"]
            track_id = target_info.get("track_id", "?")
            distance = depth_estimator.estimate_distance(target_info["height"])
            
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
            cv2.circle(frame, target_info["center"], 5, (0, 0, 255), -1)
            
            info_text = f"ID:{track_id} | Dist:{distance}m"
            cv2.putText(frame, info_text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
            cv2.line(frame, (frame_width//2, frame_height//2), target_info["center"], (255, 0, 0), 2)

        elif active_target_pos:
            cv2.circle(frame, active_target_pos, 5, (128, 128, 128), -1)
            cv2.putText(frame, "GHOST TRACKING", (active_target_pos[0]-50, active_target_pos[1]-10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (128, 128, 128), 2)

        cv2.putText(frame, f"FPS: {fps}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, f"Status: {agent_status}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
        cv2.putText(frame, f"CMD: [{pan_cmd}] | [{tilt_cmd}]", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

        cv2.imshow("Gimbal CV Agent - Live View", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            logger.info("Nhận lệnh thoát từ người dùng.")
            break

    streamer.stop()
    cv2.destroyAllWindows()
    logger.info("Hệ thống đã tắt an toàn.")

if __name__ == "__main__":
    main()