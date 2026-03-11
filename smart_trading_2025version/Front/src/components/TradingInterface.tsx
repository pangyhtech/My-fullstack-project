import React, { useState, useMemo } from 'react';
import styled from 'styled-components';
import { Form, Input, Button, Select, message, Divider, Space, Card } from 'antd';
import { ArrowUpOutlined, ArrowDownOutlined, TableOutlined } from '@ant-design/icons';

const { Option } = Select;

const TradingContainer = styled.div`
  background: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
`;

const OrderForm = styled(Form)`
  max-width: 400px;
`;

const GridTradingCard = styled(Card)`
  margin-top: 20px;
`;

interface TradingInterfaceProps {
  tradingPair: string;
  apiKey: string;
  secretKey: string;
  passphrase: string;
}

const TradingInterface: React.FC<TradingInterfaceProps> = ({
  tradingPair,
  apiKey,
  secretKey,
  passphrase,
}) => {
  const [form] = Form.useForm();
  const [gridForm] = Form.useForm();
  const [loading, setLoading] = useState(false);
  const [gridLoading, setGridLoading] = useState(false);

  // 动态获取币种名称
  const baseCurrency = useMemo(() => tradingPair.split('/')[0], [tradingPair]);
  const quoteCurrency = useMemo(() => tradingPair.split('/')[1], [tradingPair]);

  // 处理普通委托下单
  const handleSubmit = async (values: any) => {
    try {
      setLoading(true);
      const orderData: any = {
        tradingPair,
        direction: values.direction,
        orderType: values.orderType,
        apiKey,
        secretKey,
        passphrase,
      };
      
      // 针对不同订单类型设置不同参数
      if (values.orderType === 'limit') {
        // 限价单
        orderData.amount = values.amount;
        orderData.price = values.price;
      } else if (values.orderType === 'market') {
        if (values.direction === 'buy') {
          // 市价买单 - 指定总金额而不是数量
          // 估算：总金额 = 数量 * 估计价格
          // 我们传递原始数量，后端会处理转换
          orderData.amount = values.amount;
        } else {
          // 市价卖单 - 直接使用数量
          orderData.amount = values.amount;
        }
      }

      const response = await fetch('http://localhost:5001/api/place_order', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(orderData),
      });

      const result = await response.json();
      
      if (response.ok) {
        message.success('订单提交成功！');
        form.resetFields(['amount', 'price']);
      } else {
        message.error(`订单提交失败: ${result.error}`);
      }
    } catch (error) {
      message.error('订单提交失败，请检查网络连接');
    } finally {
      setLoading(false);
    }
  };

  // 处理网格交易下单
  const handleGridSubmit = async (values: any) => {
    try {
      setGridLoading(true);
      
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
        gridForm.resetFields();
      } else {
        const errors = [];
        if (!sellResponse.ok) errors.push(`卖单失败: ${sellResult.error || '未知错误'}`);
        if (!buyResponse.ok) errors.push(`买单失败: ${buyResult.error || '未知错误'}`);
        message.error(`网格交易创建失败: ${errors.join('; ')}`);
      }
    } catch (error) {
      message.error('网格交易创建失败，请检查网络连接');
    } finally {
      setGridLoading(false);
    }
  };

  return (
    <TradingContainer>
      <h2>交易 {tradingPair}</h2>
      <OrderForm
        form={form}
        onFinish={handleSubmit}
        layout="vertical"
        initialValues={{
          direction: 'buy',
          orderType: 'market',
          amount: '0.01',
        }}
      >
        <Form.Item
          name="direction"
          label="交易方向"
          rules={[{ required: true, message: '请选择交易方向' }]}
        >
          <Select>
            <Option value="buy">买入 {baseCurrency}</Option>
            <Option value="sell">卖出 {baseCurrency}</Option>
          </Select>
        </Form.Item>

        <Form.Item
          name="orderType"
          label="订单类型"
          rules={[{ required: true, message: '请选择订单类型' }]}
        >
          <Select>
            <Option value="market">市价单</Option>
            <Option value="limit">限价单</Option>
          </Select>
        </Form.Item>

        <Form.Item
          name="amount"
          label={`数量 (${baseCurrency})`}
          rules={[{ required: true, message: `请输入${baseCurrency}数量` }]}
        >
          <Input type="number" step="0.0001" min="0" suffix={baseCurrency} />
        </Form.Item>

        <Form.Item
          noStyle
          shouldUpdate={(prevValues, currentValues) => 
            prevValues.orderType !== currentValues.orderType
          }
        >
          {({ getFieldValue }) => 
            getFieldValue('orderType') === 'limit' && (
              <Form.Item
                name="price"
                label={`价格 (${quoteCurrency})`}
                rules={[{ required: true, message: `请输入价格 (${quoteCurrency})` }]}
              >
                <Input type="number" step="0.1" min="0" suffix={quoteCurrency} />
              </Form.Item>
            )
          }
        </Form.Item>

        <Form.Item>
          <Button 
            type="primary" 
            htmlType="submit" 
            loading={loading}
            icon={form.getFieldValue('direction') === 'buy' ? <ArrowUpOutlined /> : <ArrowDownOutlined />}
            style={{ 
              width: '100%',
              backgroundColor: form.getFieldValue('direction') === 'buy' ? '#52c41a' : '#f5222d'
            }}
          >
            {form.getFieldValue('direction') === 'buy' ? `买入${baseCurrency}` : `卖出${baseCurrency}`}
          </Button>
        </Form.Item>
      </OrderForm>
      
      <Divider>网格交易</Divider>
      
      <GridTradingCard title="网格交易配置">
        <Form
          form={gridForm}
          layout="vertical"
          onFinish={handleGridSubmit}
          initialValues={{
            lowPrice: '',
            highPrice: '',
            gridAmount: '0.01'
          }}
        >
          <Form.Item
            name="lowPrice"
            label={`最低价格 (${quoteCurrency})`}
            rules={[{ required: true, message: '请输入最低价格' }]}
          >
            <Input type="number" step="0.1" min="0" suffix={quoteCurrency} />
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
            <Input type="number" step="0.1" min="0" suffix={quoteCurrency} />
          </Form.Item>
          
          <Form.Item
            name="gridAmount"
            label={`委托数量 (${baseCurrency})`}
            rules={[{ required: true, message: '请输入委托数量' }]}
          >
            <Input type="number" step="0.0001" min="0" suffix={baseCurrency} />
          </Form.Item>
          
          <Form.Item>
            <Button
              type="primary"
              htmlType="submit"
              loading={gridLoading}
              icon={<TableOutlined />}
              style={{ width: '100%' }}
            >
              生成网格
            </Button>
          </Form.Item>
        </Form>
      </GridTradingCard>
    </TradingContainer>
  );
};

export default TradingInterface; 