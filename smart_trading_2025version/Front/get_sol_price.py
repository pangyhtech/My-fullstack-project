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

# 获取SOL/JPY的市场价格
trading_pair = "SOL-JPY"
timestamp = get_timestamp()
request_path = f'/api/spot/v3/tickers/{trading_pair}'
sign_str = sign(timestamp, 'GET', request_path, SECRET_KEY)
headers = get_headers(API_KEY, sign_str, timestamp, PASSPHRASE)

try:
    response = requests.get(
        f'https://www.okcoin.jp{request_path}',
        headers=headers
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"\nSOL/JPY 当前市场价格：")
        print(f"最新成交价: {data.get('last')} JPY")
        print(f"买一价: {data.get('bid')} JPY")
        print(f"卖一价: {data.get('ask')} JPY")
        print(f"24小时最高: {data.get('high_24h')} JPY")
        print(f"24小时最低: {data.get('low_24h')} JPY")
        print(f"24小时成交量: {data.get('volume_24h')} SOL")
    else:
        print(f"获取价格失败: {response.status_code}")
        print(f"错误信息: {response.text}")
except Exception as e:
    print(f"发生错误: {str(e)}")
