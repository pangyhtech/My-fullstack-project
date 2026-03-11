import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import TradingInterface from './components/TradingInterface';
import OrderList from './components/OrderList';
import 'antd/dist/reset.css';
import { message, Select } from 'antd';

const { Option } = Select;

const AppContainer = styled.div`
  max-width: 1400px;
  margin: 0 auto;
  padding: 20px;
`;

const MainContent = styled.div`
  display: flex;
  gap: 20px;
`;

const RightPanel = styled.div`
  flex: 1;
`;

const StatusBar = styled.div`
  margin-bottom: 10px;
  padding: 10px;
  background-color: #f5f5f5;
  border-radius: 4px;
  font-size: 12px;
`;

const TRADING_PAIRS = [
  'BTC/JPY', 'ETH/JPY', 'SOL/JPY', 'ADA/JPY', 'XRP/JPY', 'DOT/JPY',
  'MATIC/JPY', 'AVAX/JPY', 'LINK/JPY', 'UNI/JPY', 'AAVE/JPY', 'ATOM/JPY',
  'LTC/JPY', 'BCH/JPY', 'DOGE/JPY', 'SHIB/JPY', 'TRX/JPY', 'EOS/JPY',
  'XLM/JPY', 'XTZ/JPY', 'ALGO/JPY', 'FIL/JPY', 'NEAR/JPY', 'APT/JPY',
  'OP/JPY', 'ARB/JPY', 'SUI/JPY', 'INJ/JPY', 'GMX/JPY', 'SNX/JPY'
];

const API_CONFIG = {
  apiKey: 'a2735c47-015a-43f7-a166-2dee8f44ef0a',
  secretKey: 'A6C573D0B57C8D1FBC1A2D6EC6F1ED64',
  passphrase: 'Panggouzi666'
};

const App: React.FC = () => {
  const [serverStatus, setServerStatus] = useState<string>('未连接');
  const [tradingPair, setTradingPair] = useState<string>('BTC/JPY');

  // 测试API连接
  useEffect(() => {
    const testApiConnection = async () => {
      try {
        const response = await fetch('http://localhost:5001/api/health');
        if (response.ok) {
          const data = await response.json();
          setServerStatus('已连接');
          console.log('API服务器连接成功:', data);
        } else {
          setServerStatus('连接失败');
          console.error('API服务器连接失败:', response.status);
        }
      } catch (error) {
        setServerStatus('连接错误');
        console.error('API服务器连接错误:', error);
        message.error('无法连接到后端服务，请确保服务已启动');
      }
    };
    testApiConnection();
  }, []);

  return (
    <AppContainer>
      <StatusBar>
        <div>服务器状态: <span style={{ color: serverStatus === '已连接' ? 'green' : 'red' }}>{serverStatus}</span></div>
        <div>
          当前交易对: 
          <Select
            value={tradingPair}
            onChange={setTradingPair}
            style={{ width: 120, marginLeft: 8 }}
            size="small"
          >
            {TRADING_PAIRS.map(pair => (
              <Option key={pair} value={pair}>{pair}</Option>
            ))}
          </Select>
        </div>
        <div>API状态: <span style={{ color: 'green' }}>已配置</span></div>
      </StatusBar>
      <MainContent>
        <RightPanel>
          <TradingInterface
            tradingPair={tradingPair}
            apiKey={API_CONFIG.apiKey}
            secretKey={API_CONFIG.secretKey}
            passphrase={API_CONFIG.passphrase}
          />
          <OrderList tradingPair={tradingPair} />
        </RightPanel>
      </MainContent>
    </AppContainer>
  );
};

export default App; 