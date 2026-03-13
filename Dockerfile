# 1. Sử dụng Python phiên bản 3.11 làm nền tảng
FROM python:3.11-slim

# 2. Cài đặt các thư viện hệ thống cần thiết cho OpenCV và GUI
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libgtk2.0-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# 3. Thiết lập thư mục làm việc trong Container
WORKDIR /app

# 4. Copy file requirements vào và cài đặt thư viện Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy toàn bộ code dự án vào thư mục /app
COPY . .

# 6. Lệnh mặc định khi khởi chạy Container
CMD ["python", "main.py"]