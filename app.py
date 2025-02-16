import re
from flask import Flask, render_template, request, redirect, url_for
import json
import requests
import subprocess
import os

app = Flask(__name__)
def is_streamlit_running():
    try:
        response = requests.get("http://localhost:8080")
        return response.status_code == 200
    except requests.ConnectionError:
        return False
        
DATA_PROCESSED_FILE = 'dataduocxuly.json'

# Từ điển chuyển đổi tên thành phố không dấu sang có dấu
city_dictionary = {
    'hochiminh': 'Ho Chi Minh',
    'hanoi': 'Ha Noi',
    'danang': 'Da Nang',
    'haiphong': 'Hai Phong',
    'nhatrang': 'Nha Trang',
    'cantho': 'Can Tho',
    'dalat': 'Da Lat',
    'quangninh': 'Quang Ninh',
    'bariavungtau': 'Ba Ria - Vung Tau',
    'binhduong': 'Binh Duong',
    'phuquoc': 'Phu Quoc',
    'namdinh': 'Nam Dinh',
    'vinh': 'Vinh',
    'thaibinh': 'Thai Binh',
    'thanhhoa': 'Thanh Hoa',
    'nghean': 'Nghe An',
    'quangnam': 'Quang Nam',
    'hagiang': 'Ha Giang',
    'yenbai': 'Yen Bai',
    'langson': 'Lang Son',
    'hue': 'Hue',
    'phutho': 'Phu Tho',
    'ninhbinh': 'Ninh Binh',
    'bacninh': 'Bac Ninh',
    'quangtri': 'Quang Tri',
    'phuyen': 'Phu Yen',
    'kontum': 'Kon Tum',
    'gialai': 'Gia Lai',
    'daklak': 'Dak Lak',
    'daknong': 'Dak Nong',
    'lamdong': 'Lam Dong',
    'khanhhoa': 'Khanh Hoa',
    'bentre': 'Ben Tre',
    'travinh': 'Tra Vinh',
    'vinhlong': 'Vinh Long',
    'haugiang': 'Hau Giang',
    'soctrang': 'Soc Trang',
    'kiengiang': 'Kien Giang',
    'angiang': 'An Giang',
    'dongnai': 'Dong Nai',
    'binhthuan': 'Binh Thuan',
    'tiengiang': 'Tien Giang',
    'ninhthuan': 'Ninh Thuan',
    'quangngai': 'Quang Ngai',
    'baclieu': 'Bac Lieu',
    'camau': 'Ca Mau',
    'hanam': 'Ha Nam',
    'haiduong': 'Hai Duong',
    'hoabinh': 'Hoa Binh',
    'thuathienhue': 'Thua Thien Hue',
    'tuyenquang': 'Tuyen Quang',
    'vinhphuc': 'Vinh Phuc',
    'bacgiang': 'Bac Giang',
}

def normalize_city_name(city):
    # Chuyển thành chữ thường, xóa dấu và khoảng trắng
    city = city.lower()
    city = re.sub(r'[áàảãạăắằẳẵặâấầẩẫậ]', 'a', city)
    city = re.sub(r'[éèẻẽẹêếềểễệ]', 'e', city)
    city = re.sub(r'[íìỉĩị]', 'i', city)
    city = re.sub(r'[óòỏõọôốồổỗộơớờởỡợ]', 'o', city)
    city = re.sub(r'[úùủũụưứừửữự]', 'u', city)
    city = re.sub(r'[ýỳỷỹỵ]', 'y', city)
    city = re.sub(r'[đ]', 'd', city)
    city = re.sub(r'\s+', '', city)  # Loại bỏ khoảng trắng
    return city
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/weather', methods=['GET', 'POST'])
def index():
    error_message = None
    if request.method == 'POST':
        city = request.form['city'].strip()
        city = normalize_city_name(city)  # Chuẩn hóa tên thành phố

        # Kiểm tra nếu tên thành phố có trong từ điển
        if city in city_dictionary:
            city = city_dictionary[city]  # Chuyển đổi tên thành phố
        else:
            error_message = (
                "Tên thành phố không hợp lệ. "
                "Vui lòng nhập lại và đảm bảo tên thành phố có trong danh sách."
            )
            return render_template('index.html', error=error_message)

        command = f"./check_api.sh '{city}'"
        result = subprocess.run(command, shell=True, capture_output=True, text=True)

        if result.returncode != 0:
            error_message = f"Error: {result.stderr}"
            return render_template('index.html', error=error_message)

        subprocess.run("./xulydulieu.sh", shell=True)
        return redirect(url_for('show_data'))

    return render_template('index.html', error=error_message)

@app.route('/data', methods=['GET'])
def show_data():
    current_data = {}
    forecast_data = []

    if os.path.exists(DATA_PROCESSED_FILE):
        with open(DATA_PROCESSED_FILE, 'r') as f:
            try:
                data = json.load(f)
                if data:
                    current_data = data[0]
                    forecast_data = data[1:]
            except json.JSONDecodeError:
                return render_template('data.html', current=None, forecast=None, error="Error decoding processed data.")

    return render_template('data.html', current=current_data, forecast=forecast_data)

@app.route('/chatbot', methods=['GET', 'POST'])
def run_chatbot(port=8052):  # Thay đổi port tại đây nếu cần
    if not is_streamlit_running():
        command = ["streamlit", "run", "chatbot.py", f"--server.port={port}"]
        subprocess.Popen(command)
    
    return redirect(f"http://localhost:{port}")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
