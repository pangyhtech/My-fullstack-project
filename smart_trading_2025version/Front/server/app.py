from flask import Flask, request, jsonify
import hmac
import base64
import json
import logging
import requests
from datetime import datetime
from flask_cors import CORS
import sys
import os

# 添加SDK路径
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'okcoin-python-sdk-api'))
import okcoin.spot_api as spot

app = Flask(__name__)
CORS(app)  # 启用CORS支持

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok"})

@app.route('/api/place_order', methods=['POST'])
def place_order():
    try:
        data = request.json
        logger.info(f"收到订单请求: {json.dumps(data, ensure_ascii=False)}")
        
        # 验证必填字段 - 移除API密钥相关字段的验证
        required_fields = ['tradingPair', 'direction', 'orderType']
        
        # 判断订单类型，添加相应的必填字段
        if data.get('orderType') == 'limit':
            required_fields.extend(['amount', 'price'])
        elif data.get('orderType') == 'market':
            if data.get('direction') == 'buy':
                # 市价买单需要总金额
                if not (data.get('total') or data.get('notional')):
                    # 如果前端未提供，并且非amount，则报错
                    if not data.get('amount'):
                        missing_fields = ['total/notional/amount']
                        error_msg = f"市价买单缺少必填字段: {', '.join(missing_fields)}"
                        logger.error(error_msg)
                        return jsonify({'error': error_msg}), 400
            else:
                # 市价卖单需要数量
                required_fields.append('amount')
                
        missing_fields = [field for field in required_fields if not data.get(field)]
        if missing_fields:
            error_msg = f"缺少必填字段: {', '.join(missing_fields)}"
            logger.error(error_msg)
            return jsonify({'error': error_msg}), 400
            
        # 转换交易对格式
        trading_pair = data.get('tradingPair')
        if '/' in trading_pair:
            instrument_id = trading_pair.replace('/', '-')
        else:
            instrument_id = trading_pair
        
        # 使用预设的API密钥信息，无需前端传递
        api_key = API_KEY
        secret_key = SECRET_KEY
        passphrase = PASSPHRASE
        
        # 使用SDK初始化spot API
        spotAPI = spot.SpotAPI(api_key, secret_key, passphrase, False)
        
        # 处理虚拟交易对MEME_INDEX/JPY
        if trading_pair == 'MEME_INDEX/JPY' or instrument_id == 'MEME_INDEX-JPY':
            logger.info(f"处理虚拟交易对MEME_INDEX/JPY，批量下单")
            # 定义组成交易对及其固定数量
            meme_components = [
                {"pair": "SHIB-JPY", "amount": 50000},
                {"pair": "DOGE-JPY", "amount": 10},
                {"pair": "PEPE-JPY", "amount": 100000},
            ]
            
            # 用户选择的方向(买入/卖出)
            direction = data.get('direction')
            all_orders_results = []
            
            for component in meme_components:
                # 构建该组件的下单参数
                component_params = {
                    'instrument_id': component["pair"],
                    'side': direction,
                    'type': data.get('orderType'),
                    'order_type': '0',
                    'client_oid': ''
                }
                
                # 根据订单类型设置不同参数
                if data.get('orderType') == 'limit':
                    # 限价单：使用固定数量和用户指定的价格
                    component_params['size'] = str(component["amount"])
                    component_params['price'] = data.get('price')
                elif data.get('orderType') == 'market':
                    if direction == 'buy':
                        # 市价买单：估算所需金额
                        # 假设SHIB价格0.5日元，DOGE价格10日元，PEPE价格0.1日元
                        mock_prices = {
                            "SHIB-JPY": 0.5,
                            "DOGE-JPY": 10,
                            "PEPE-JPY": 0.1
                        }
                        if component["pair"] in mock_prices:
                            estimated_price = mock_prices[component["pair"]]
                            # 计算购买固定数量所需的金额
                            notional_amount = component["amount"] * estimated_price
                            component_params['notional'] = str(notional_amount)
                        else:
                            # 如果没有模拟价格，使用一个安全的默认值
                            component_params['notional'] = "1000"
                    else:
                        # 市价卖单：直接使用固定数量
                        component_params['size'] = str(component["amount"])
                
                # 移除空值
                component_params = {k: v for k, v in component_params.items() if v is not None and v != ''}
                
                logger.info(f"批量下单组件 {component['pair']}，参数: {json.dumps(component_params, ensure_ascii=False)}")
                
                try:
                    # 执行下单
                    result = spotAPI.take_order(**component_params)
                    all_orders_results.append({
                        "pair": component["pair"],
                        "result": result
                    })
                    logger.info(f"组件 {component['pair']} 下单结果: {json.dumps(result, ensure_ascii=False)}")
                except Exception as e:
                    error_msg = f"组件 {component['pair']} 下单失败: {str(e)}"
                    logger.error(error_msg)
                    all_orders_results.append({
                        "pair": component["pair"],
                        "error": error_msg
                    })
            
            # 返回所有组件的下单结果
            return jsonify({
                "meme_index": "MEME_INDEX/JPY",
                "components_results": all_orders_results,
                "result": True,
                "message": "MEME指数批量下单完成"
            })
        
        # 设置SDK下单参数
        sdk_params = {
            'instrument_id': instrument_id,
            'side': data.get('direction'),  # 买卖方向: buy或sell
            'type': data.get('orderType'),  # 订单类型: limit或market
            'order_type': '0',              # 委托类型: 0-普通委托
            'client_oid': ''
        }
        
        # 记录订单类型映射情况
        logger.info(f"订单类型映射: 前端orderType={data.get('orderType')} -> SDK type={sdk_params['type']}")
        logger.info(f"买卖方向映射: 前端direction={data.get('direction')} -> SDK side={sdk_params['side']}")
        
        # 根据订单类型设置不同参数
        if data.get('orderType') == 'limit':
            # 限价单需要数量和价格
            sdk_params['size'] = data.get('amount')
            sdk_params['price'] = data.get('price')
        elif data.get('orderType') == 'market':
            if data.get('direction') == 'buy':
                # 市价买单 - 为确保购买精确数量，我们使用"限价单"模拟"市价单"
                amount = data.get('amount', '0.01')
                
                # 修改订单类型为限价单
                sdk_params['type'] = 'limit'
                
                # 设置一个高于市价的价格（当前SOL约25,000-30,000 JPY，设置32,000作为安全值）
                sdk_params['price'] = '32000'
                
                # 设置精确购买数量
                sdk_params['size'] = amount
                
                # 移除notional参数，限价单不使用此参数
                if 'notional' in sdk_params:
                    del sdk_params['notional']
                
                logger.info(f"使用限价单模拟市价买单，精确数量: {amount} {data.get('tradingPair').split('/')[0]}")
                logger.info(f"设置较高价格: 32000 JPY 确保成交")
            else:
                # 市价卖单需要数量(size)
                sdk_params['size'] = data.get('amount')
                logger.info(f"市价卖单，使用数量: {sdk_params.get('size')}")
        
        # 移除空值
        sdk_params = {k: v for k, v in sdk_params.items() if v is not None and v != ''}
        
        logger.info(f"使用SDK下单，参数: {json.dumps(sdk_params, ensure_ascii=False)}")
        
        # 使用SDK执行下单
        result = spotAPI.take_order(**sdk_params)
        
        logger.info(f"SDK下单结果: {json.dumps(result, ensure_ascii=False)}")
        
        if result.get('result'):
            return jsonify(result)
        else:
            error_msg = f"下单失败: {result.get('error_message') or '未知错误'}"
            logger.error(error_msg)
            return jsonify({'error': error_msg}), 500
            
    except Exception as e:
        error_msg = f"处理订单时发生错误: {str(e)}"
        logger.error(error_msg)
        return jsonify({'error': error_msg}), 500

@app.route('/api/order_list', methods=['POST'])
def order_list():
    try:
        data = request.json
        # 使用预设的API密钥
        api_key = API_KEY
        secret_key = SECRET_KEY
        passphrase = PASSPHRASE
        trading_pair = data.get('tradingPair', None)
        
        # 虚拟交易对MEME_INDEX的特殊处理
        if trading_pair == 'MEME_INDEX/JPY' or trading_pair == 'MEME_INDEX-JPY':
            logger.info(f"处理虚拟交易对MEME_INDEX/JPY的订单查询")
            # 为虚拟交易对返回空结果，因为它实际上是三个交易对的组合
            return jsonify([])
        
        # 转换交易对格式
        instrument_id = None
        if trading_pair:
            if '/' in trading_pair:
                instrument_id = trading_pair.replace('/', '-')
            else:
                instrument_id = trading_pair
        
        # 使用SDK初始化spot API
        spotAPI = spot.SpotAPI(api_key, secret_key, passphrase, False)
        
        # 增加查询参数: limit参数指定获取的订单数量，最大为100
        # 获取当前未成交订单
        logger.info(f"正在查询当前委托，交易对: {instrument_id}")
        result = spotAPI.get_orders_pending(instrument_id=instrument_id if instrument_id else '', limit='100')
        
        # 处理SDK返回的元组格式数据
        # OKCoin SDK返回的是(订单列表, 分页信息)的元组格式
        if isinstance(result, tuple) and len(result) > 0:
            logger.info(f"成功获取当前委托列表，返回元组格式数据")
            # 提取元组中的订单列表
            orders = result[0] if len(result) > 0 and isinstance(result[0], list) else []
            logger.info(f"当前委托列表共 {len(orders)} 条记录")
            
            # 检查每条记录的created_at字段
            for order in orders:
                if isinstance(order, dict) and 'created_at' in order:
                    logger.info(f"订单 {order.get('order_id')} created_at: {order.get('created_at')}")
            
            # 直接返回原始元组，前端可以处理第一个元素
            return jsonify(result)
        elif isinstance(result, list):
            logger.info(f"成功获取当前委托列表，共 {len(result)} 条记录")
            return jsonify(result)
        else:
            logger.warning(f"当前委托结果格式异常: {type(result)}")
            # 返回空列表避免前端错误
            return jsonify([])
    except Exception as e:
        error_msg = f"查询委托时发生错误: {str(e)}"
        logger.error(error_msg)
        return jsonify({'error': error_msg}), 500

@app.route('/api/order_history', methods=['POST'])
def order_history():
    try:
        data = request.json
        # 使用预设的API密钥
        api_key = API_KEY
        secret_key = SECRET_KEY
        passphrase = PASSPHRASE
        trading_pair = data.get('tradingPair', None)
        
        # 虚拟交易对MEME_INDEX的特殊处理
        if trading_pair == 'MEME_INDEX/JPY' or trading_pair == 'MEME_INDEX-JPY':
            logger.info(f"处理虚拟交易对MEME_INDEX/JPY的历史订单查询")
            # 为虚拟交易对返回空结果，因为它实际上是三个交易对的组合
            return jsonify([])
        
        # 转换交易对格式
        instrument_id = None
        if trading_pair:
            if '/' in trading_pair:
                instrument_id = trading_pair.replace('/', '-')
            else:
                instrument_id = trading_pair
        
        # 使用SDK初始化spot API
        spotAPI = spot.SpotAPI(api_key, secret_key, passphrase, False)
        
        # 获取历史订单 - state=7表示已完成状态的订单
        # 增加查询参数: limit参数指定获取的订单数量，最大为100
        logger.info(f"正在查询历史委托，交易对: {instrument_id}")
        result = spotAPI.get_orders_list(instrument_id=instrument_id if instrument_id else '', state='7', limit='100')
        
        # 处理SDK返回的元组格式数据
        # OKCoin SDK返回的是(订单列表, 分页信息)的元组格式
        if isinstance(result, tuple) and len(result) > 0:
            logger.info(f"成功获取历史委托列表，返回元组格式数据")
            # 提取元组中的订单列表
            orders = result[0] if len(result) > 0 and isinstance(result[0], list) else []
            logger.info(f"历史委托列表共 {len(orders)} 条记录")
            
            # 检查每条记录的created_at字段
            for order in orders:
                if isinstance(order, dict) and 'created_at' in order:
                    logger.info(f"历史订单 {order.get('order_id')} created_at: {order.get('created_at')}")
            
            # 直接返回原始元组，前端可以处理第一个元素
            return jsonify(result)
        elif isinstance(result, list):
            logger.info(f"成功获取历史委托列表，共 {len(result)} 条记录")
            return jsonify(result)
        else:
            logger.warning(f"历史委托结果格式异常: {type(result)}")
            # 返回空列表避免前端错误
            return jsonify([])
    except Exception as e:
        error_msg = f"查询历史委托时发生错误: {str(e)}"
        logger.error(error_msg)
        return jsonify({'error': error_msg}), 500

@app.route('/api/account_balance', methods=['POST'])
def account_balance():
    try:
        data = request.json
        # 使用预设的API密钥
        api_key = API_KEY
        secret_key = SECRET_KEY
        passphrase = PASSPHRASE
        
        # 生成签名
        timestamp = get_timestamp()
        request_path = '/api/spot/v3/accounts'
        sign_str = sign(timestamp, 'GET', request_path, secret_key)
        headers = get_headers(api_key, sign_str, timestamp, passphrase)
        
        # 发送请求到OKCoin
        url = 'https://www.okcoin.jp' + request_path
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            # 只返回sol和jpy的资产
            sol = next((item for item in data if item['currency'].lower() == 'sol'), None)
            jpy = next((item for item in data if item['currency'].lower() == 'jpy'), None)
            return jsonify({'sol': sol, 'jpy': jpy})
        else:
            error_msg = f"查询资产失败: {response.status_code} - {response.text}"
            logger.error(error_msg)
            return jsonify({'error': error_msg}), 500
    except Exception as e:
        error_msg = f"查询资产时发生错误: {str(e)}"
        logger.error(error_msg)
        return jsonify({'error': error_msg}), 500

@app.route('/api/cancel_order', methods=['POST'])
def cancel_order():
    try:
        data = request.json
        # 使用预设的API密钥
        api_key = API_KEY
        secret_key = SECRET_KEY
        passphrase = PASSPHRASE
        
        # 获取订单ID和交易对
        order_id = data.get('order_id')
        instrument_id = data.get('instrument_id')
        
        if not order_id or not instrument_id:
            error_msg = "缺少必填字段: order_id 或 instrument_id"
            logger.error(error_msg)
            return jsonify({'error': error_msg}), 400
        
        # 使用SDK初始化spot API
        spotAPI = spot.SpotAPI(api_key, secret_key, passphrase, False)
        
        # 取消订单
        result = spotAPI.revoke_order(instrument_id=instrument_id, order_id=order_id)
        
        logger.info(f"取消订单结果: {json.dumps(result, ensure_ascii=False) if isinstance(result, dict) else '非字典类型结果'}")
        
        return jsonify(result)
    except Exception as e:
        error_msg = f"取消订单时发生错误: {str(e)}"
        logger.error(error_msg)
        return jsonify({'error': error_msg}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True) 