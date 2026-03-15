#  Gimbal CV Agent: Autonomous Target Tracking System

[![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![AI Model](https://img.shields.io/badge/Model-YOLOv11-green.svg)](https://github.com/ultralytics/ultralytics)
[![Architecture](https://img.shields.io/badge/Architecture-Modular_OOP-orange.svg)](#)
[![Docker](https://img.shields.io/badge/Docker-Edge_Ready-2496ED.svg)](https://www.docker.com/)

A professional-grade **Computer Vision AI Agent** designed for real-time object tracking on Edge AI devices (UAVs, Maritime vessels). Built with a robust **Modular OOP Architecture**, this system features a "Short-term Memory" mechanism for occlusion handling and runs flawlessly in Headless mode using Docker.


---

##  Key Features

* **Real-time Perception:** Powered by optimized YOLOv11 inference for high-speed, accurate target detection.
* **Ghost Tracking (Memory Module):** Predicts and maintains target trajectories using short-term memory when the subject is temporarily lost or occluded.
* **Headless Edge Processing:** Automatically processes video streams in the background without requiring a GUI, saving the annotated output with telemetry data (XVID `.avi` format).
* **PID Control Simulation:** Translates visual coordinate errors into actionable Gimbal Pan/Tilt commands with customizable deadzones.
* **Dockerized & Reproducible:** Fully containerized environment ensuring zero dependency conflicts across different hardware.

---

##  Project Structure

```text
Gimbal-CV-Agent/
├── configs/                # YAML Configuration files
│   ├── system_config.yaml  # Camera source, FPS, Target class, Deadzones
│   ├── model_params.yaml   # AI Hyperparameters
│   └── gimbal_pid.yaml     # Physical motor PID settings
│
├── data/                   
│   ├── logs/               # Agent execution logs
│   └── sample_streams/     # Input videos & Output Auto-recordings (.avi)
│
├── models/                 
│   └── detection/          # YOLOv8 weight files (.pt)
│
├── src/                    # Core OOP Modules
│   ├── ingestion/          # Video/RTSP Stream handling with auto-resize
│   ├── perception/         # AI Inference wrapper (Detector)
│   ├── agent/              # Logic Engine & Short-term Memory
│   ├── control/            # Gimbal kinematics and Alert systems
│   └── core/               # Metrics (FPS) & Custom Loggers
│
├── main.py                 # Main execution pipeline
├── docker-compose.yml      # Multi-container orchestration
├── Dockerfile              # Headless Edge Linux environment
└── requirements.txt        # Python dependencies
