class AlertSystem:
    def send_alert(self, message):
        # Nơi cấu hình gọi API gửi tin nhắn Telegram, Zalo hoặc Email
        print(f"[CẢNH BÁO KHẨN] -> Gửi tới Trạm mặt đất: {message}")