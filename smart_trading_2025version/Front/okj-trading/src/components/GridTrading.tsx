import React, { useState } from 'react';
import styled from 'styled-components';
import { Form, Input, Button, message, Card } from 'antd';
import { TableOutlined } from '@ant-design/icons';

const GridContainer = styled.div`
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  margin-top: 20px;
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

interface GridTradingProps {
  tradingPair: string;
  apiKey: string;
  secretKey: string;
  passphrase: string;
}

const GridTrading: React.FC<GridTradingProps> = ({
  tradingPair,
  apiKey,
  secretKey,
  passphrase,
}) => {
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);
  
  // 动态获取币种名称
  const baseCurrency = tradingPair.split('/')[0];
  const quoteCurrency = tradingPair.split('/')[1];

  const handleGridSubmit = async (values: any) => {
    try {
      setLoading(true);
      
      // 1. 创建高价卖出委托
      const sellOrderData = {
        tradingPair,
        direction: 'sell',
        orderType: 'limit',
        amount: values.gridAmount,
        price: values.highPrice,
        apiKey,
        secretKey,
        passphrase,
      };
      
      // 2. 创建低价买入委托
      const buyOrderData = {
        tradingPair,
        direction: 'buy',
        orderType: 'limit',
        amount: values.gridAmount,
        price: values.lowPrice,
        apiKey,
        secretKey,
        passphrase,
      };
      
      // 顺序发送两个委托
      const sellResponse = await fetch('http://localhost:5001/api/place_order', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(sellOrderData),
      });
      
      const sellResult = await sellResponse.json();
      
      const buyResponse = await fetch('http://localhost:5001/api/place_order', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(buyOrderData),
      });
      
      const buyResult = await buyResponse.json();
      
      if (sellResponse.ok && buyResponse.ok) {
        message.success('网格交易委托创建成功！');
        form.resetFields();
      } else {
        const errors = [];
        if (!sellResponse.ok) errors.push(`卖单失败: ${sellResult.error || '未知错误'}`);
        if (!buyResponse.ok) errors.push(`买单失败: ${buyResult.error || '未知错误'}`);
        message.error(`网格交易创建失败: ${errors.join('; ')}`);
      }
    } catch (error) {
      message.error('网格交易创建失败，请检查网络连接');
      console.error('网格交易错误:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <GridContainer>
      <StyledCard
        title="网格交易"
        bordered={false}
      >
        <Form
          form={form}
          layout="vertical"
          onFinish={handleGridSubmit}
          initialValues={{
            lowPrice: '',
            highPrice: '',
            gridAmount: '0.01'
          }}
          size="small"
        >
          <Form.Item
            name="lowPrice"
            label={`最低价格 (${quoteCurrency})`}
            rules={[{ required: true, message: '请输入最低价格' }]}
          >
            <Input type="number" step="0.1" min="0" placeholder={`输入最低买入价格 (${quoteCurrency})`} />
          </Form.Item>
          
          <Form.Item
            name="highPrice"
            label={`最高价格 (${quoteCurrency})`}
            rules={[
              { required: true, message: '请输入最高价格' },
              ({ getFieldValue }) => ({
                validator(_, value) {
                  if (!value || !getFieldValue('lowPrice') || parseFloat(value) > parseFloat(getFieldValue('lowPrice'))) {
                    return Promise.resolve();
                  }
                  return Promise.reject(new Error('最高价格必须高于最低价格'));
                },
              }),
            ]}
          >
            <Input type="number" step="0.1" min="0" placeholder={`输入最高卖出价格 (${quoteCurrency})`} />
          </Form.Item>
          
          <Form.Item
            name="gridAmount"
            label={`委托数量 (${baseCurrency})`}
            rules={[{ required: true, message: '请输入委托数量' }]}
          >
            <Input type="number" step="0.0001" min="0" placeholder={`输入每笔委托的数量 (${baseCurrency})`} />
          </Form.Item>
          
          <Form.Item>
            <Button
              type="primary"
              htmlType="submit"
              loading={loading}
              icon={<TableOutlined />}
              block
            >
              生成网格
            </Button>
          </Form.Item>
        </Form>
      </StyledCard>
    </GridContainer>
  );
};

export default GridTrading; 