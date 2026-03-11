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
    
    # 测试不同的API密钥和Passphrase组合
    API_KEY = "a2735c47-015a-43f7-a166-2dee8f44ef0a"
    SECRET_KEY = "A6C573D0B57C8D1FBC1A2D6EC6F1ED64"
    
    # 尝试不同的Passphrase
    for passphrase in ["", "Panggouzi666", "", "panggouzi666"]:
        print(f"\n尝试Passphrase: {passphrase}")
        try:
            spotAPI = spot.SpotAPI(API_KEY, SECRET_KEY, passphrase, False)
            print(f"成功创建SpotAPI实例，使用Passphrase: {passphrase}")
            
            # 尝试获取所有账户信息（这个API一般较容易通过）
            try:
                print("尝试获取账户信息...")
                accounts = spotAPI._request_without_params("GET", "/api/spot/v3/accounts")
                print(f"账户信息请求结果: {accounts if isinstance(accounts, str) else '成功'}")
                
                # 如果成功，则尝试获取历史订单
                try:
                    print("尝试获取历史订单...")
                    result = spotAPI.get_orders_list(instrument_id='SOL-JPY', state='7')
                    print(f"历史订单结果: {result if isinstance(result, str) else '成功'}")
                    # 找到正确的Passphrase，退出循环
                    print(f"找到正确的Passphrase: {passphrase}")
                    break
                except Exception as order_e:
                    print(f"获取历史订单失败: {order_e}")
            except Exception as req_e:
                print(f"请求账户信息失败: {req_e}")
        except Exception as api_e:
            print(f"创建SpotAPI实例失败: {api_e}")
except Exception as e:
    print("导入SDK失败:", e) 