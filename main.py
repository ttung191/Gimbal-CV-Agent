import cv2
import yaml
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
    logger.info("Initializing Gimbal CV Agent ...")

    try:
        config = load_config()
    except Exception as e:
        logger.error(f"Config loading error: {e}")
        return

    logger.info("Initializing Ingestion (Camera)...")
    camera = StreamReader(
        source=config['camera']['source'],
        width=config['camera']['width'],
        height=config['camera']['height']
    ).start()

    logger.info("Initializing Perception (YOLOv8)...")
    detector = Detector(
        conf_thresh=config['target']['confidence_threshold'],
        target_class=config['target']['class_id']
    )

    logger.info("Initializing Control (Gimbal)...")
    gimbal = GimbalController(
        frame_width=config['camera']['width'],
        frame_height=config['camera']['height'],
        deadzone=config['gimbal']['deadzone']
    )

    logger.info("Initializing Agent (Memory & Decision)...")
    memory = ShortTermMemory(max_size=30)
    decision_engine = DecisionEngine(memory_module=memory)
    
    fps_counter = FPSCounter()

    logger.info("=== SYSTEM READY ===")
    logger.info("Press 'q' on the Camera window to exit.")

    while True:
        ret, frame = camera.read_frame()
        if not ret:
            logger.error("Camera connection lost.")
            break

        current_fps = fps_counter.update()
        target_info = detector.detect(frame)
        target_center = target_info["center"] if target_info else None

        status_message = decision_engine.evaluate(target_center)
        
        pan, tilt = "STOP", "STOP"
        
        if target_info:
            bbox = target_info["bbox"]
            center = target_info["center"]
            
            cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (0, 255, 0), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)
            
            pan, tilt, _, _ = gimbal.calculate_commands(center)
            
        else:
            last_known_center = memory.get_last_known_position()
            
            if last_known_center:
                cv2.circle(frame, last_known_center, 8, (0, 255, 255), 2)
                cv2.putText(frame, "GHOST TARGET", (last_known_center[0]+10, last_known_center[1]), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
                
                pan, tilt, _, _ = gimbal.calculate_commands(last_known_center)

        # Draw HUD (Heads Up Display)
        color_status = (0, 255, 0) if target_info else ((0, 255, 255) if memory.get_last_known_position() else (0, 165, 255))
        
        cv2.putText(frame, f"STATUS: {status_message}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color_status, 2)
        cv2.putText(frame, f"PAN: {pan} | TILT: {tilt}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
        cv2.putText(frame, f"FPS: {current_fps}", (config['camera']['width'] - 120, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 2)

        cv2.drawMarker(frame, (gimbal.center_x, gimbal.center_y), (0, 255, 255), cv2.MARKER_CROSS, 20, 1)

        cv2.imshow("Gimbal CV Agent - Flawless", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            logger.info("User requested shutdown.")
            break

    camera.stop()
    cv2.destroyAllWindows()
    logger.info("System shut down safely.")

if __name__ == "__main__":
    main()