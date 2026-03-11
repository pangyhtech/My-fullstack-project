import React, { useState } from 'react';
import styled from 'styled-components';
import { Form, Input, Select, Button, message, Card } from 'antd';
import { SaveOutlined } from '@ant-design/icons';

const { Option } = Select;

const ConfigContainer = styled.div`
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
`;

const Title = styled.h2`
  text-align: center;
  margin-bottom: 24px;
  color: #333;
  font-size: 18px;
`;

const StyledCard = styled(Card)`
  .ant-card-head {
    padding: 0 16px;
    min-height: 48px;
  }
  .ant-card-body {
    padding: 16px;
  }
`;

// 定义交易对数据
const TRADING_PAIRS = [
  { value: 'BTC/JPY', label: 'BTC/JPY' },
  { value: 'ETH/JPY', label: 'ETH/JPY' },
  { value: 'ADA/JPY', label: 'ADA/JPY' },
  { value: 'XRP/JPY', label: 'XRP/JPY' },
  { value: 'DOT/JPY', label: 'DOT/JPY' },
  { value: 'SOL/JPY', label: 'SOL/JPY' },
  { value: 'MATIC/JPY', label: 'MATIC/JPY' },
  { value: 'AVAX/JPY', label: 'AVAX/JPY' },
  { value: 'LINK/JPY', label: 'LINK/JPY' },
  { value: 'UNI/JPY', label: 'UNI/JPY' },
  { value: 'AAVE/JPY', label: 'AAVE/JPY' },
  { value: 'ATOM/JPY', label: 'ATOM/JPY' },
  { value: 'LTC/JPY', label: 'LTC/JPY' },
  { value: 'BCH/JPY', label: 'BCH/JPY' },
  { value: 'DOGE/JPY', label: 'DOGE/JPY' },
  { value: 'SHIB/JPY', label: 'SHIB/JPY' },
  { value: 'TRX/JPY', label: 'TRX/JPY' },
  { value: 'EOS/JPY', label: 'EOS/JPY' },
  { value: 'XLM/JPY', label: 'XLM/JPY' },
  { value: 'XTZ/JPY', label: 'XTZ/JPY' },
  { value: 'ALGO/JPY', label: 'ALGO/JPY' },
  { value: 'FIL/JPY', label: 'FIL/JPY' },
  { value: 'NEAR/JPY', label: 'NEAR/JPY' },
  { value: 'APT/JPY', label: 'APT/JPY' },
  { value: 'OP/JPY', label: 'OP/JPY' },
  { value: 'ARB/JPY', label: 'ARB/JPY' },
  { value: 'SUI/JPY', label: 'SUI/JPY' },
  { value: 'INJ/JPY', label: 'INJ/JPY' },
  { value: 'GMX/JPY', label: 'GMX/JPY' },
  { value: 'SNX/JPY', label: 'SNX/JPY' },
  { value: 'MEME_INDEX/JPY', label: 'MEME_INDEX/JPY (每份固定买入: 50000SHIB+10DOGE+100000PEPE)' },
];

interface ApiConfigProps {
  onConfigComplete: (config: {
    tradingPair: string;
    apiKey: string;
    secretKey: string;
    passphrase: string;
  }) => void;
}

const ApiConfig: React.FC<ApiConfigProps> = ({ onConfigComplete }) => {
  const [form] = Form.useForm();

  // 在组件挂载时自动设置默认API密钥并提交（只运行一次）
  React.useEffect(() => {
    // 默认API配置
    const defaultConfig = {
      tradingPair: 'SOL/JPY',
      apiKey: 'a2735c47-015a-43f7-a166-2dee8f44ef0a',
      secretKey: 'A6C573D0B57C8D1FBC1A2D6EC6F1ED64',
      passphrase: 'Panggouzi666'
    };
    
    // 设置表单值
    form.setFieldsValue(defaultConfig);
    
    // 自动提交配置 - 使用setTimeout避免渲染循环
    setTimeout(() => {
      onConfigComplete(defaultConfig);
      message.success('API配置已自动加载');
    }, 0);
    
    // 空依赖数组确保此effect只运行一次
  }, []);

  const handleSubmit = (values: any) => {
    // 在实际应用中，这里应该添加API密钥的验证逻辑
    onConfigComplete({
      tradingPair: values.tradingPair,
      apiKey: values.apiKey,
      secretKey: values.secretKey,
      passphrase: values.passphrase,
    });
    message.success('API配置已保存');
  };

  return (
    <ConfigContainer>
      <StyledCard
        title="API配置"
        bordered={false}
      >
        <Form
          form={form}
          layout="vertical"
          onFinish={handleSubmit}
          initialValues={{ tradingPair: 'BTC/JPY' }}
          size="small"
        >
          <Form.Item
            name="tradingPair"
            label="交易对"
            rules={[{ required: true, message: '请选择交易对' }]}
          >
            <Select
              showSearch
              placeholder="选择交易对"
              optionFilterProp="children"
              filterOption={(input, option) =>
                (option?.label as string)?.toLowerCase().includes(input.toLowerCase())
              }
              onChange={(value) => {
                const values = form.getFieldsValue();
                onConfigComplete({
                  ...values,
                  tradingPair: value,
                });
              }}
            >
              {TRADING_PAIRS.map(pair => (
                <Option key={pair.value} value={pair.value}>
                  {pair.label}
                </Option>
              ))}
            </Select>
          </Form.Item>

          <Form.Item
            name="apiKey"
            label="API Key"
            rules={[{ required: true, message: '请输入API Key' }]}
          >
            <Input.Password placeholder="请输入API Key" />
          </Form.Item>

          <Form.Item
            name="secretKey"
            label="Secret Key"
            rules={[{ required: true, message: '请输入Secret Key' }]}
          >
            <Input.Password placeholder="请输入Secret Key" />
          </Form.Item>

          <Form.Item
            name="passphrase"
            label="Passphrase"
            rules={[{ required: true, message: '请输入Passphrase' }]}
          >
            <Input.Password placeholder="请输入Passphrase" />
          </Form.Item>

          <Form.Item>
            <Button type="primary" htmlType="submit" icon={<SaveOutlined />} block>
              保存配置
            </Button>
          </Form.Item>
        </Form>
      </StyledCard>
    </ConfigContainer>
  );
};

export default ApiConfig; 