from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os
import json
import time
import base64
import hmac
import requests
import logging
from typing import Optional

# 配置日志
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[logging.StreamHandler()])
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

BASE_URL = 'https://www.okcoin.jp'

def get_timestamp():
    return str(int(time.time() * 1000))

def sign(timestamp: str, method: str, request_path: str, secret_key: str, body: str = "") -> str:
    if not body:
        body = ""
    
    message = timestamp + method + request_path + body
    mac = hmac.new(
        bytes(secret_key, encoding='utf8'),
        bytes(message, encoding='utf-8'),
        digestmod='sha256'
    )
    d = mac.digest()
    return base64.b64encode(d).decode('utf-8')

def get_headers(api_key: str, signed_string: str, timestamp: str, passphrase: str):
    return {
        'OK-ACCESS-KEY': api_key,
        'OK-ACCESS-SIGN': signed_string,
        'OK-ACCESS-TIMESTAMP': timestamp,
        'OK-ACCESS-PASSPHRASE': passphrase,
        'Content-Type': 'application/json'
    }

@app.route('/api/place_order', methods=['POST'])
def place_order():
    try:
        data = request.json
        logger.info(f"收到订单请求: {json.dumps(data, ensure_ascii=False)}")
        
        # 验证必填字段
        required_fields = ['apiKey', 'secretKey', 'passphrase', 'tradingPair', 'direction', 'orderType', 'amount']
        missing_fields = [field for field in required_fields if not data.get(field)]
        if missing_fields:
            error_msg = f"缺少必填字段: {', '.join(missing_fields)}"
            logger.error(error_msg)
            return jsonify({'error': error_msg}), 400
            
        api_key = data.get('apiKey')
        secret_key = data.get('secretKey')
        passphrase = data.get('passphrase')
        trading_pair = data.get('tradingPair')
        
        # 转换交易对格式
        if '/' in trading_pair:
            instrument_id = trading_pair.replace('/', '-')  # 例如 "BTC/JPY" -> "BTC-JPY"
        else:
            instrument_id = trading_pair  # 可能已经是正确格式
        
        # 打印关键信息（不打印敏感信息）
        logger.info(f"交易对: {trading_pair} -> {instrument_id}")
        logger.info(f"订单类型: {data.get('orderType')}")
        logger.info(f"方向: {data.get('direction')}")
        logger.info(f"数量: {data.get('amount')}")
        
        # 订单参数
        order_data = {
            'instrument_id': instrument_id,
            'side': data.get('direction'),  # 'buy' or 'sell'
            'size': data.get('amount'),
            'type': data.get('orderType'),  # 'limit' or 'market'
        }

        # 根据订单类型添加特定参数
        if order_data['type'] == 'limit':
            if not data.get('price'):
                return jsonify({'error': '限价单需要提供价格'}), 400
            order_data['price'] = data.get('price')
            order_data['order_type'] = '0'  # 普通限价单
        elif order_data['type'] == 'market':
            if order_data['side'] == 'buy':
                order_data['notional'] = data.get('amount')  # 市价买入使用notional（总金额）
                del order_data['size']
            order_data['order_type'] = '0'  # 普通市价单
        elif order_data['type'] == 'advanced_limit':
            if not data.get('price'):
                return jsonify({'error': '高级限价单需要提供价格'}), 400
            order_data['price'] = data.get('price')
            # 设置高级限价单的执行机制
            time_in_force = data.get('timeInForce')
            if time_in_force == 'post_only':
                order_data['order_type'] = '1'
            elif time_in_force == 'fill_or_kill':
                order_data['order_type'] = '2'
            elif time_in_force == 'immediate_or_cancel':
                order_data['order_type'] = '3'
        elif order_data['type'] == 'stop':
            if not data.get('price'):
                return jsonify({'error': '止盈止损单需要提供委托价格'}), 400
            if not data.get('triggerPrice'):
                return jsonify({'error': '止盈止损单需要提供触发价格'}), 400
            order_data['type'] = 'limit'  # 止盈止损实际上是限价单
            order_data['price'] = data.get('price')  # 委托价格
            order_data['trigger_price'] = data.get('triggerPrice')  # 触发价格
            order_data['order_type'] = '0'
        else:
            return jsonify({'error': f"不支持的订单类型: {order_data['type']}"}), 400

        logger.info(f"准备发送的订单数据: {json.dumps(order_data, ensure_ascii=False)}")
        
        # 模拟模式，不实际发送API请求
        mock_mode = True
        if mock_mode:
            logger.info("模拟模式: 不实际发送API请求")
            return jsonify({
                "result": True,
                "order_id": "12345678",
                "client_oid": "",
                "error_code": "",
                "error_message": "",
                "order_type": order_data.get('order_type', '0')
            })
        
        # 实际模式: 生成签名并发送请求
        timestamp = get_timestamp()
        body = json.dumps(order_data)
        request_path = '/api/spot/v3/orders'
        sign_str = sign(timestamp, 'POST', request_path, secret_key, body)
        
        # 请求参数日志（不记录敏感信息）
        logger.info(f"请求路径: {request_path}")
        logger.info(f"请求方法: POST")
        logger.info(f"请求体: {body}")
        
        # 发送请求
        headers = get_headers(api_key, sign_str, timestamp, passphrase)
        logger.info("正在发送API请求...")
        
        try:
            response = requests.post(
                BASE_URL + request_path,
                headers=headers,
                data=body
            )
            
            response_json = response.json()
            logger.info(f"API响应: {json.dumps(response_json, ensure_ascii=False)}")
            
            # 检查API错误
            if response.status_code != 200:
                error_msg = f"API请求失败: HTTP {response.status_code}, {response_json.get('error_message', '未知错误')}"
                logger.error(error_msg)
                return jsonify({'error': error_msg}), response.status_code
                
            return jsonify(response_json)
        except requests.exceptions.RequestException as e:
            error_msg = f"API请求异常: {str(e)}"
            logger.error(error_msg)
            return jsonify({'error': error_msg}), 500
    
    except Exception as e:
        logger.error(f"处理订单请求时出错: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok', 'message': '服务器正常运行'})

if __name__ == '__main__':
    logger.info("OKCoin 交易API服务器启动，监听5001端口...")
    logger.info(f"模拟模式: {'开启' if True else '关闭'}")
    logger.info(f"API基础URL: {BASE_URL}")
    app.run(host='0.0.0.0', port=5001, debug=True) 