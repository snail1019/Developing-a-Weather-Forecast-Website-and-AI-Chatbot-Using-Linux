#!/bin/bash

# Định nghĩa biến cho API key và URL
API_KEY=""  #your key 
BASE_URL="http://api.weatherapi.com/v1"  

# Lấy tên thành phố từ tham số truyền vào script
city="$1"  # Tên thành phố được truyền từ Flask

# Kiểm tra xem tên thành phố có được truyền vào hay không
if [ -z "$city" ]; then
    echo "City name is missing. Please provide a valid city name."
    exit 1
fi

# Kiểm tra nếu tên thành phố có chứa khoảng trắng
if [[ "$city" == *" "* ]]; then
    mahoaten_city=$(echo "$city" | sed 's/ /%20/g')  # Mã hóa khoảng trắng
else
    mahoaten_city="$city"  # Nếu không có khoảng trắng, giữ nguyên tên thành phố
fi

# Tạo URL đầy đủ
API_URL_HIENTAI="${BASE_URL}/current.json?key=${API_KEY}&q=${mahoaten_city}&aqi=no"
API_URL_DUDOAN="${BASE_URL}/forecast.json?key=${API_KEY}&q=${mahoaten_city}&days=7&aqi=no&alerts=no"

# In ra URL để kiểm tra
echo "Current API URL: $API_URL_HIENTAI"
echo "Forecast API URL: $API_URL_DUDOAN"

# Gửi yêu cầu và lưu dữ liệu vào tệp
current_response=$(curl -s -w "%{http_code}" -o current_weather.json "$API_URL_HIENTAI")
future_response=$(curl -s -w "%{http_code}" -o forecast_weather.json "$API_URL_DUDOAN")

# Kiểm tra mã trạng thái API hiện tại
if [ "$current_response" -eq 200 ]; then
    echo "Current weather API is valid and accessible."
else
    echo "Current weather API returned status code: $current_response"
    echo "Response: $(cat current_weather.json)"  # Hiển thị nội dung tệp để xem lỗi
fi

# Kiểm tra mã trạng thái API dự báo
if [ "$future_response" -eq 200 ]; then
    echo "Forecast weather API is valid and accessible."
else
    echo "Forecast weather API returned status code: $future_response"
    echo "Response: $(cat forecast_weather.json)"  # Hiển thị nội dung tệp để xem lỗi
fi
