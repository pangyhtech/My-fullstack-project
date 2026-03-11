import sys
import os
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 添加SDK路径
print("当前工作目录:", os.getcwd())
sdk_path = os.path.join(os.path.dirname(__file__), '..', 'okcoin-python-sdk-api')
print("SDK路径:", sdk_path)
sys.path.append(sdk_path)

try:
    import okcoin.spot_api as spot
    print("成功导入SDK")
    
    # 测试API密钥
    API_KEY = "a2735c47-015a-43f7-a166-2dee8f44ef0a"
    SECRET_KEY = "A6C573D0B57C8D1FBC1A2D6EC6F1ED64"
    PASSPHRASE = "Panggouzi666"
    
    try:
        spotAPI = spot.SpotAPI(API_KEY, SECRET_KEY, PASSPHRASE, False)
        print("成功创建SpotAPI实例")
        
        # 尝试获取历史订单
        try:
            result = spotAPI.get_orders_list(instrument_id='SOL-JPY', state='7')
            print("获取历史订单结果:", result)
        except Exception as order_e:
            print("获取历史订单失败:", order_e)
    except Exception as api_e:
        print("创建SpotAPI实例失败:", api_e)
except Exception as e:
    print("导入SDK失败:", e) 