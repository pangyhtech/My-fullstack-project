import requests
import hmac
import base64
import json
from datetime import datetime

# API配置
API_KEY = "a2735c47-015a-43f7-a166-2dee8f44ef0a"
SECRET_KEY = "A6C573D0B57C8D1FBC1A2D6EC6F1ED64"
PASSPHRASE = "Panggouzi666"

def get_timestamp():
    return datetime.utcnow().isoformat()[:-3] + 'Z'

def sign(timestamp: str, method: str, request_path: str, secret_key: str, body: str = "") -> str:
    if not body:
        body = ""
    message = timestamp + method + request_path + body
    mac = hmac.new(
        bytes(secret_key, encoding='utf8'),
        bytes(message, encoding='utf-8'),
        digestmod='sha256'
    )
    return base64.b64encode(mac.digest()).decode('utf-8')

def get_headers(api_key: str, signed_string: str, timestamp: str, passphrase: str):
    return {
        'OK-ACCESS-KEY': api_key,
        'OK-ACCESS-SIGN': signed_string,
        'OK-ACCESS-TIMESTAMP': timestamp,
        'OK-ACCESS-PASSPHRASE': passphrase,
        'Content-Type': 'application/json'
    }

# 测试连接
try:
    # 获取服务器时间
    timestamp = get_timestamp()
    request_path = '/api/general/v3/time'
    sign_str = sign(timestamp, 'GET', request_path, SECRET_KEY)
    headers = get_headers(API_KEY, sign_str, timestamp, PASSPHRASE)
    
    print("正在连接OKCoin Japan服务器...")
    response = requests.get(
        'https://www.okcoin.jp' + request_path,
        headers=headers
    )
    
    if response.status_code == 200:
        print("连接成功！")
        print(f"服务器时间: {response.json()}")
    else:
        print(f"连接失败: {response.status_code}")
        print(f"错误信息: {response.text}")
except Exception as e:
    print(f"连接错误: {str(e)}")
