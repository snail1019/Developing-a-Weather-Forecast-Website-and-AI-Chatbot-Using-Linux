#Sử dụng image chính thức Python từ Docker Hub
FROM python:3.9-slim

# Thiết lập biến môi trường
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Đặt thư mục làm việc trong container
WORKDIR /code

# Sao chép tệp requirements và cài đặt dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Sao chép mã nguồn của ứng dụng vào thư mục làm việc
COPY . /code/

# Cài đặt supervisor
RUN apt-get update && apt-get install -y supervisor

# Sao chép tệp cấu hình supervisor vào container
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Mở cổng cho cả hai ứng dụng
EXPOSE 8000 8080
# Chạy supervisor
CMD ["supervisord", "-n"]
