import cv2
import yaml
import os
from src.core import AgentLogger, FPSCounter
from src.ingestion import StreamReader
from src.perception import Detector
from src.agent import ShortTermMemory, DecisionEngine
from src.control import GimbalController

def load_config(config_path="configs/system_config.yaml"):
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def main():
    logger = AgentLogger(name="GimbalAgent")
    logger.info("Initializing Gimbal CV Agent (Docker/Recording Version)...")

    try:
        config = load_config()
    except Exception as e:
        logger.error(f"Config loading error: {e}")
        return

    # 1. Khởi tạo Ingestion (Đọc Stream/Video)
    logger.info("Initializing Ingestion (Camera/Video)...")
    camera = StreamReader(
        source=config['camera']['source'],
        width=config['camera']['width'],
        height=config['camera']['height']
    ).start()

    # 2. Khởi tạo Perception (YOLOv8)
    logger.info("Initializing Perception (YOLOv8)...")
    detector = Detector(
        conf_thresh=config['target']['confidence_threshold'],
        target_class=config['target']['class_id']
    )

    # 3. Khởi tạo Control (Gimbal)
    logger.info("Initializing Control (Gimbal)...")
    gimbal = GimbalController(
        frame_width=config['camera']['width'],
        frame_height=config['camera']['height'],
        deadzone=config['gimbal']['deadzone']
    )

    # 4. Khởi tạo Agent (Trí nhớ & Ra quyết định)
    logger.info("Initializing Agent (Memory & Decision)...")
    memory = ShortTermMemory(max_size=30)
    decision_engine = DecisionEngine(memory_module=memory)
    fps_counter = FPSCounter()

    # --- KHỞI TẠO TÍNH NĂNG RECORDING ---
    os.makedirs('data/sample_streams', exist_ok=True)
    
    output_path = 'data/sample_streams/agent_record.avi' 
    fourcc = cv2.VideoWriter_fourcc(*'XVID') 
    
    # Lấy chính xác số FPS từ file config thay vì hardcode 20.0
    video_fps = config['camera']['fps']
    out_video = cv2.VideoWriter(output_path, fourcc, video_fps, (config['camera']['width'], config['camera']['height']))
    logger.info(f"Video sẽ được tự động lưu tại: {output_path} với {video_fps} FPS")
    # ------------------------------------

    logger.info("=== SYSTEM READY. RUNNING IN BACKGROUND... ===")

    frame_count = 0
    max_frames = 200 # Chạy ngầm 200 frame

    while frame_count < max_frames:
        ret, frame = camera.read_frame()
        if not ret:
            logger.warning("Không đọc được frame hoặc hết video.")
            break

        # Ép khung hình về đúng chuẩn cấu hình
        frame = cv2.resize(frame, (config['camera']['width'], config['camera']['height']))

        current_fps = fps_counter.update()
        target_info = detector.detect(frame)
        target_center = target_info["center"] if target_info else None

        status_message = decision_engine.evaluate(target_center)
        pan, tilt = "STOP", "STOP"
        
        if target_info:
            bbox = target_info["bbox"]
            center = target_info["center"]
            
            # Vẽ Box Xanh và Tâm
            cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (0, 255, 0), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)
            
            pan, tilt, _, _ = gimbal.calculate_commands(center)
        else:
            last_known = memory.get_last_known_position()
            if last_known:
                # Vẽ Ghost Target Vàng
                cv2.circle(frame, last_known, 8, (0, 255, 255), 2)
                cv2.putText(frame, "GHOST TARGET", (last_known[0]+10, last_known[1]), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
                pan, tilt, _, _ = gimbal.calculate_commands(last_known)

        # Vẽ HUD
        color_status = (0, 255, 0) if target_info else ((0, 255, 255) if memory.get_last_known_position() else (0, 165, 255))
        cv2.putText(frame, f"STATUS: {status_message}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color_status, 2)
        cv2.putText(frame, f"PAN: {pan} | TILT: {tilt}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
        cv2.putText(frame, f"FPS: {current_fps}", (config['camera']['width'] - 120, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 2)
        cv2.drawMarker(frame, (gimbal.center_x, gimbal.center_y), (0, 255, 255), cv2.MARKER_CROSS, 20, 1)

        # LƯU FRAME VÀO VIDEO FILE
        out_video.write(frame)
        frame_count += 1
        
        # In log tiến độ
        if frame_count % 30 == 0:
            logger.info(f"Đã xử lý {frame_count}/{max_frames} frames. Status: {status_message}")

    # Dọn dẹp tài nguyên
    camera.stop()
    out_video.release()
    logger.info("Đã ghi hình xong. Hệ thống tắt an toàn.")

if __name__ == "__main__":
    main()