import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import { Input, Button, Select, Slider, Radio, Card, message, Space, Divider } from 'antd';
import { ArrowUpOutlined, ArrowDownOutlined } from '@ant-design/icons';

const { Option } = Select;

const TradingContainer = styled.div`
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  padding: 20px;
`;

const PriceInput = styled(Input)`
  margin-bottom: 16px;
  .ant-input-group-addon {
    background: #f5f5f5;
    color: #666;
  }
`;

const AmountInput = styled(Input)`
  margin-bottom: 16px;
  .ant-input-group-addon {
    background: #f5f5f5;
    color: #666;
  }
`;

const TotalInput = styled(Input)`
  margin-bottom: 16px;
  .ant-input-group-addon {
    background: #f5f5f5;
    color: #666;
  }
`;

const StyledSlider = styled(Slider)`
  margin: 16px 0;
`;

const OrderTypeSelector = styled(Radio.Group)`
  margin-bottom: 16px;
  width: 100%;
  display: flex;
  justify-content: space-between;
  
  .ant-radio-button-wrapper {
    flex: 1;
    text-align: center;
  }
`;

const ActionButton = styled(Button)`
  height: 40px;
  font-size: 16px;
  margin-top: 16px;
`;

const BuyButton = styled(ActionButton)`
  background: #00b578;
  border-color: #00b578;
  &:hover {
    background: #009966;
    border-color: #009966;
  }
`;

const SellButton = styled(ActionButton)`
  background: #ff4d4f;
  border-color: #ff4d4f;
  &:hover {
    background: #ff7875;
    border-color: #ff7875;
  }
`;

const PercentageButtons = styled.div`
  display: flex;
  gap: 8px;
  margin: 8px 0;
`;

const PercentageButton = styled(Button)`
  flex: 1;
`;

const StyledSelect = styled(Select)`
  width: 100%;
  margin-bottom: 16px;
`;

const DirectionSelector = styled(Radio.Group)`
  margin-bottom: 16px;
  width: 100%;
  display: flex;
  justify-content: space-between;
  
  .ant-radio-button-wrapper {
    flex: 1;
    text-align: center;
  }
`;

// 添加日志组件
const LogContainer = styled.div`
  margin-top: 20px;
  padding: 10px;
  background: #f5f5f5;
  border-radius: 4px;
  max-height: 150px;
  overflow-y: auto;
`;

const LogEntry = styled.div`
  font-family: monospace;
  font-size: 12px;
  margin-bottom: 4px;
`;

interface TradingInterfaceProps {
  tradingPair: string;
  apiKey: string;
  secretKey: string;
  passphrase: string;
}

type OrderType = 'limit' | 'market' | 'advanced_limit' | 'stop';
type TimeInForce = 'post_only' | 'fill_or_kill' | 'immediate_or_cancel';
type Direction = 'buy' | 'sell';
type StopDirection = 'one_way' | 'two_way';

const ORDER_TYPES = [
  { value: 'limit', label: '限价委托' },
  { value: 'market', label: '市价委托' },
  { value: 'advanced_limit', label: '高级限价委托' },
  { value: 'stop', label: '止盈止损' },
];

const STOP_DIRECTIONS = [
  { value: 'one_way', label: '单向' },
  { value: 'two_way', label: '双向' },
];

const TradingInterface: React.FC<TradingInterfaceProps> = ({ 
  tradingPair,
  apiKey,
  secretKey,
  passphrase 
}) => {
  // 添加baseCurrency状态
  const [baseCurrency, setBaseCurrency] = useState<string>(tradingPair.split('/')[0] || 'BTC');
  const [direction, setDirection] = useState<Direction>('buy');
  const [orderType, setOrderType] = useState<OrderType>('limit');
  const [timeInForce, setTimeInForce] = useState<TimeInForce>('post_only');
  const [stopDirection, setStopDirection] = useState<StopDirection>('one_way');
  const [price, setPrice] = useState<string>('');
  const [triggerPrice, setTriggerPrice] = useState<string>('');
  const [amount, setAmount] = useState<string>('');
  const [total, setTotal] = useState<string>('');
  const [percentage, setPercentage] = useState<number>(0);
  const [logs, setLogs] = useState<string[]>([]);
  const [isSubmitting, setIsSubmitting] = useState<boolean>(false);
  
  // 当交易对变化时更新baseCurrency
  useEffect(() => {
    if (tradingPair) {
      const newBaseCurrency = tradingPair.split('/')[0];
      setBaseCurrency(newBaseCurrency);
      addLog(`交易对已更新: ${tradingPair}，基础货币: ${newBaseCurrency}`);
    }
  }, [tradingPair]);

  // 添加日志函数
  const addLog = (log: string) => {
    setLogs(prevLogs => [...prevLogs, `${new Date().toISOString()}: ${log}`]);
  };

  // 获取显示用的币种名称
  const getDisplayCurrency = () => {
    if (baseCurrency === 'MEME_INDEX') {
      return 'MEME指数';
    }
    return baseCurrency;
  };
  
  // 获取数量字段说明
  const getAmountLabel = () => {
    if (baseCurrency === 'MEME_INDEX') {
      return "份数(固定买入50000SHIB+10DOGE+100000PEPE)";
    }
    return "数量";
  };

  // 测试API连接
  useEffect(() => {
    const testApiConnection = async () => {
      try {
        const response = await fetch('http://localhost:5001/api/health');
        const data = await response.json();
        addLog(`API连接测试: ${data.message}`);
      } catch (error: any) {
        addLog(`API连接测试失败: ${error.message || '未知错误'}`);
        message.error('无法连接到后端服务，请确保服务已启动');
      }
    };

    testApiConnection();
  }, []);

  const handlePriceChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setPrice(e.target.value);
  };

  const handleTriggerPriceChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setTriggerPrice(e.target.value);
  };

  const handleAmountChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setAmount(e.target.value);
    if (price && orderType !== 'market') {
      setTotal((parseFloat(e.target.value) * parseFloat(price)).toString());
    }
  };

  const handleTotalChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setTotal(e.target.value);
    if (price) {
      setAmount((parseFloat(e.target.value) / parseFloat(price)).toString());
    }
  };

  const handlePercentageChange = (value: number) => {
    setPercentage(value);
    // 这里需要根据用户余额计算实际数量
    message.info(`设置使用${value}%的可用余额`);
  };

  const validateForm = (): boolean => {
    // 验证API信息
    if (!apiKey || !secretKey || !passphrase) {
      message.error('请提供完整的API配置信息');
      addLog('错误: API配置信息不完整');
      return false;
    }

    // 验证交易对
    if (!tradingPair) {
      message.error('请选择交易对');
      addLog('错误: 未选择交易对');
      return false;
    }

    // 验证金额
    if (!amount || parseFloat(amount) <= 0) {
      message.error('请输入有效的数量');
      addLog('错误: 数量无效');
      return false;
    }

    // 根据订单类型验证价格
    if ((orderType === 'limit' || orderType === 'advanced_limit' || orderType === 'stop') && 
        (!price || parseFloat(price) <= 0)) {
      message.error('请输入有效的价格');
      addLog('错误: 价格无效');
      return false;
    }

    // 验证止盈止损的触发价格
    if (orderType === 'stop' && (!triggerPrice || parseFloat(triggerPrice) <= 0)) {
      message.error('请输入有效的触发价格');
      addLog('错误: 触发价格无效');
      return false;
    }

    return true;
  };

  const handleSubmit = async () => {
    // 验证表单
    if (!validateForm()) return;

    setIsSubmitting(true);
    addLog(`开始提交${direction === 'buy' ? '买入' : '卖出'}订单: ${tradingPair}`);

    try {
      const orderData = {
        apiKey,
        secretKey,
        passphrase,
        tradingPair,
        direction,
        orderType,
        timeInForce,
        stopDirection,
        price,
        triggerPrice,
        amount,
        total,
      };

      addLog(`准备发送数据到API: ${JSON.stringify({
        tradingPair,
        direction,
        orderType,
        amount,
        price: price || '市价'
      })}`);

      const response = await fetch('http://localhost:5001/api/place_order', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(orderData),
      });

      if (!response.ok) {
        throw new Error(`HTTP错误: ${response.status}`);
      }

      const result = await response.json();
      
      addLog(`收到API响应: ${JSON.stringify(result)}`);
      
      if (result.error) {
        message.error(`下单失败: ${result.error}`);
        addLog(`下单失败: ${result.error}`);
      } else {
        message.success(`${direction === 'buy' ? '买入' : '卖出'}委托已提交，订单ID: ${result.order_id || '未知'}`);
        addLog(`下单成功! 订单ID: ${result.order_id || '未知'}`);
        
        // 清空表单
        setPrice('');
        setTriggerPrice('');
        setAmount('');
        setTotal('');
        setPercentage(0);
      }
    } catch (error: any) {
      const errorMessage = error.message || '未知错误';
      message.error(`下单失败: ${errorMessage}`);
      addLog(`下单失败: ${errorMessage}`);
      console.error('下单错误:', error);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <TradingContainer>
      <DirectionSelector value={direction} onChange={e => setDirection(e.target.value)} buttonStyle="solid">
        <Radio.Button value="buy">买入</Radio.Button>
        <Radio.Button value="sell">卖出</Radio.Button>
      </DirectionSelector>

      <StyledSelect
        value={orderType}
        onChange={value => setOrderType(value as OrderType)}
        placeholder="选择委托类型"
      >
        {ORDER_TYPES.map(type => (
          <Option key={type.value} value={type.value}>
            {type.label}
          </Option>
        ))}
      </StyledSelect>

      {orderType === 'advanced_limit' && (
        <StyledSelect
          value={timeInForce}
          onChange={value => setTimeInForce(value as TimeInForce)}
          placeholder="选择生效机制"
        >
          <Option value="post_only">只做Maker(Post only)</Option>
          <Option value="fill_or_kill">全部成交和立即生效(FillOrKill)</Option>
          <Option value="immediate_or_cancel">立即成交并取消剩余(ImmediateOrCancel)</Option>
        </StyledSelect>
      )}

      {orderType === 'stop' && (
        <>
          <StyledSelect
            value={stopDirection}
            onChange={value => setStopDirection(value as StopDirection)}
            placeholder="选择止盈止损方向"
          >
            {STOP_DIRECTIONS.map(direction => (
              <Option key={direction.value} value={direction.value}>
                {direction.label}
              </Option>
            ))}
          </StyledSelect>

          <PriceInput
            addonBefore="触发价格"
            addonAfter="JPY"
            value={triggerPrice}
            onChange={handleTriggerPriceChange}
            placeholder="请输入触发价格"
          />

          <PriceInput
            addonBefore="委托价格"
            addonAfter="JPY"
            value={price}
            onChange={handlePriceChange}
            placeholder="请输入委托价格"
          />
        </>
      )}

      {(orderType === 'limit' || orderType === 'advanced_limit') && (
        <PriceInput
          addonBefore="价格"
          addonAfter="JPY"
          value={price}
          onChange={handlePriceChange}
          placeholder="请输入价格"
        />
      )}

      <PercentageButtons>
        <PercentageButton onClick={() => handlePercentageChange(25)}>25%</PercentageButton>
        <PercentageButton onClick={() => handlePercentageChange(50)}>50%</PercentageButton>
        <PercentageButton onClick={() => handlePercentageChange(75)}>75%</PercentageButton>
        <PercentageButton onClick={() => handlePercentageChange(100)}>100%</PercentageButton>
      </PercentageButtons>

      <StyledSlider
        value={percentage}
        onChange={handlePercentageChange}
        marks={{
          0: '0%',
          25: '25%',
          50: '50%',
          75: '75%',
          100: '100%'
        }}
      />

      <AmountInput
        addonBefore={getAmountLabel()}
        addonAfter={getDisplayCurrency()}
        value={amount}
        onChange={handleAmountChange}
        placeholder="请输入数量"
      />

      {orderType !== 'market' && orderType !== 'stop' && (
        <TotalInput
          addonBefore="总额"
          addonAfter="JPY"
          value={total}
          onChange={handleTotalChange}
          placeholder="请输入总额"
        />
      )}

      <ActionButton 
        type="primary" 
        block 
        loading={isSubmitting}
        onClick={handleSubmit}
        style={{
          background: direction === 'buy' ? '#00b578' : '#ff4d4f',
          borderColor: direction === 'buy' ? '#00b578' : '#ff4d4f',
        }}
      >
        {isSubmitting ? '提交中...' : `${direction === 'buy' ? '买入' : '卖出'} ${getDisplayCurrency()}`}
      </ActionButton>

      <LogContainer>
        <h4>操作日志:</h4>
        {logs.map((log, index) => (
          <LogEntry key={index}>{log}</LogEntry>
        ))}
      </LogContainer>
    </TradingContainer>
  );
};

export default TradingInterface; 