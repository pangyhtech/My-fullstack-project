#!/usr/bin/env python3
import requests
import json

# 测试服务健康状态
def test_health():
    print("\n测试API服务器健康状态...")
    try:
        response = requests.get('http://localhost:5000/api/health')
        if response.status_code == 200:
            print("✅ 服务器连接正常")
            print(f"响应: {response.json()}")
            return True
        else:
            print(f"❌ 服务器状态异常: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 无法连接到服务器: {str(e)}")
        return False

# 测试下单API
def test_place_order():
    print("\n测试下单API...")
    
    # 测试数据
    order_data = {
        "apiKey": "test_api_key",
        "secretKey": "test_secret_key",
        "passphrase": "test_passphrase",
        "tradingPair": "ADA/JPY",
        "direction": "buy",
        "orderType": "limit",
        "price": "100",
        "amount": "10"
    }
    
    try:
        print(f"发送订单数据: {json.dumps(order_data, indent=2)}")
        response = requests.post(
            'http://localhost:5000/api/place_order',
            headers={'Content-Type': 'application/json'},
            json=order_data
        )
        
        print(f"响应状态码: {response.status_code}")
        response_json = response.json()
        print(f"响应内容: {json.dumps(response_json, indent=2)}")
        
        if response.status_code == 200 and response_json.get("result") == True:
            print("✅ 下单API测试成功")
            return True
        else:
            print(f"❌ 下单API测试失败: {response_json.get('error', '未知错误')}")
            return False
    except Exception as e:
        print(f"❌ 调用下单API时出错: {str(e)}")
        return False

if __name__ == "__main__":
    print("=== OKCoin API 测试工具 ===")
    
    # 测试健康状态
    if not test_health():
        print("\n请确保后端服务已启动，然后再运行此测试脚本")
        exit(1)
    
    # 测试下单API
    test_place_order() 