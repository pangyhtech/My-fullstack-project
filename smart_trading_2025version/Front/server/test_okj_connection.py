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

def test_connection():
    try:
        # 测试获取账户信息
        timestamp = get_timestamp()
        request_path = '/api/spot/v3/accounts'
        sign_str = sign(timestamp, 'GET', request_path, SECRET_KEY)
        headers = get_headers(API_KEY, sign_str, timestamp, PASSPHRASE)
        
        print("正在测试API连接...")
        print("请求头:", json.dumps(headers, indent=2))
        
        response = requests.get(
            'https://www.okcoin.jp' + request_path,
            headers=headers
        )
        
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        
        if response.status_code == 200:
            print("API连接成功！")
            return True
        else:
            print(f"API连接失败: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"连接错误: {str(e)}")
        return False

if __name__ == "__main__":
    test_connection() 