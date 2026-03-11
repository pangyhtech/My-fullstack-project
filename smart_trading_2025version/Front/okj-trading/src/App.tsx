import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import TradingInterface from './components/TradingInterface';
import OrderList from './components/OrderList';
import ApiConfig from './components/ApiConfig';
import GridTrading from './components/GridTrading';
import 'antd/dist/reset.css';
import { message } from 'antd';

const AppContainer = styled.div`
  max-width: 1400px;
  margin: 0 auto;
  padding: 20px;
`;

const MainContent = styled.div`
  display: flex;
  gap: 20px;
`;

const LeftPanel = styled.div`
  flex: 0 0 400px;
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

interface ApiConfigData {
  tradingPair: string;
  apiKey: string;
  secretKey: string;
  passphrase: string;
}

const App: React.FC = () => {
  const [apiConfig, setApiConfig] = useState<ApiConfigData>({
    tradingPair: 'SOL/JPY',  // 默认交易对修改为SOL/JPY
    apiKey: 'a2735c47-015a-43f7-a166-2dee8f44ef0a',  // 预设API Key
    secretKey: 'A6C573D0B57C8D1FBC1A2D6EC6F1ED64',  // 预设Secret Key
    passphrase: 'Panggouzi666',  // 预设Passphrase
  });
  const [serverStatus, setServerStatus] = useState<string>('未连接');

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

  const handleConfigComplete = (config: ApiConfigData) => {
    console.log('收到API配置:', config);
    setApiConfig(config);
    message.success(`API配置已保存，交易对: ${config.tradingPair}`);
  };

  return (
    <AppContainer>
      <StatusBar>
        <div>服务器状态: <span style={{ color: serverStatus === '已连接' ? 'green' : 'red' }}>{serverStatus}</span></div>
        <div>当前交易对: <strong>{apiConfig.tradingPair}</strong> (基础货币: <strong>{apiConfig.tradingPair.split('/')[0]}</strong>)</div>
      </StatusBar>
      <MainContent>
        <LeftPanel>
          <ApiConfig onConfigComplete={handleConfigComplete} />
          <GridTrading
            tradingPair={apiConfig.tradingPair}
            apiKey={apiConfig.apiKey}
            secretKey={apiConfig.secretKey}
            passphrase={apiConfig.passphrase}
          />
        </LeftPanel>
        <RightPanel>
          <TradingInterface
            tradingPair={apiConfig.tradingPair}
            apiKey={apiConfig.apiKey}
            secretKey={apiConfig.secretKey}
            passphrase={apiConfig.passphrase}
          />
          <OrderList tradingPair={apiConfig.tradingPair} />
        </RightPanel>
      </MainContent>
    </AppContainer>
  );
};

export default App;
