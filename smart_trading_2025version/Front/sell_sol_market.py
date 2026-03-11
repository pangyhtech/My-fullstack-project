import requests
import hmac
import base64
import json
from datetime import datetime

# API配置
API_KEY = "a2735c47-015a-43f7-a166-2dee8f44ef0a"
SECRET_KEY = "A6C573D0B57C8D1FBC1A2D6EC6F1ED64"
PASSPHRASE = "Panggouzi666"  # 更新后的Passphrase

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

# 创建市价卖单
try:
    # 订单参数
    order_data = {
        'instrument_id': 'SOL-JPY',
        'side': 'sell',
        'type': 'market',
        'size': '0.01'
    }
    
    # 生成签名
    timestamp = get_timestamp()
    request_path = '/api/spot/v3/orders'
    body = json.dumps(order_data)
    sign_str = sign(timestamp, 'POST', request_path, SECRET_KEY, body)
    headers = get_headers(API_KEY, sign_str, timestamp, PASSPHRASE)
    
    print("正在发送市价卖单...")
    print(f"交易对: SOL-JPY")
    print(f"方向: 卖出")
    print(f"数量: 0.01 SOL")
    print(f"类型: 市价单")
    
    response = requests.post(
        'https://www.okcoin.jp' + request_path,
        headers=headers,
        data=body
    )
    
    if response.status_code == 200:
        result = response.json()
        print("\n订单执行结果:")
        print(f"订单ID: {result.get('order_id')}")
        print(f"状态: {result.get('result')}")
        if result.get('error_code'):
            print(f"错误代码: {result.get('error_code')}")
            print(f"错误信息: {result.get('error_message')}")
    else:
        print(f"下单失败: {response.status_code}")
        print(f"错误信息: {response.text}")
except Exception as e:
    print(f"发生错误: {str(e)}")
