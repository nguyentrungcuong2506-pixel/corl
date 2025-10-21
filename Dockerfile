# Sử dụng Python 3.10 làm môi trường chính
FROM python:3.10-slim

# Đặt thư mục làm việc trong container
WORKDIR /app

# Copy toàn bộ file trong thư mục hiện tại vào container
COPY . .

# Cài các thư viện cần thiết
RUN pip install --no-cache-dir -r requirements.txt

# Chạy bot khi container khởi động
CMD ["python", "main.py"]
