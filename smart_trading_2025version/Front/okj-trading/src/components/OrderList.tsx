import React, { useState, useEffect, useCallback, useRef } from 'react';
import styled from 'styled-components';
import { Table, Tabs, Tag, message, Spin, Input, Button, Switch, Space, Badge, Tooltip } from 'antd';
import { SearchOutlined, ReloadOutlined, SyncOutlined } from '@ant-design/icons';

const { TabPane } = Tabs;

const OrderListContainer = styled.div`
  margin-top: 20px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  padding: 20px;
`;

const ControlBar = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
`;

const SearchContainer = styled.div`
  display: flex;
  gap: 8px;
`;

const RefreshContainer = styled.div`
  display: flex;
  align-items: center;
  gap: 8px;
`;

// 添加调试模式容器样式
const DebugContainer = styled.div`
  margin-top: 10px;
  padding: 10px;
  background: #f5f5f5;
  border-radius: 4px;
  overflow: auto;
  max-height: 300px;
  white-space: pre-wrap;
  font-family: monospace;
  font-size: 12px;
`;

interface OrderListProps {
  tradingPair?: string;
}

const OrderList: React.FC<OrderListProps> = ({ tradingPair = 'BTC/JPY' }) => {
  const [activeOrders, setActiveOrders] = useState<any[]>([]);
  const [historyOrders, setHistoryOrders] = useState<any[]>([]);
  const [loadingActive, setLoadingActive] = useState<boolean>(false);
  const [loadingHistory, setLoadingHistory] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  
  // 新增状态
  const [searchText, setSearchText] = useState<string>('');
  const [autoRefresh, setAutoRefresh] = useState<boolean>(true);
  const [refreshInterval, setRefreshInterval] = useState<number>(30); // 30秒刷新一次
  const [lastRefreshTime, setLastRefreshTime] = useState<Date>(new Date());
  const intervalRef = useRef<NodeJS.Timeout | null>(null);
  const [activeOrdersPaging, setActiveOrdersPaging] = useState({
    current: 1,
    pageSize: 5,
    total: 0
  });
  const [historyOrdersPaging, setHistoryOrdersPaging] = useState({
    current: 1,
    pageSize: 5,
    total: 0
  });
  
  // 添加调试模式状态
  const [debugMode, setDebugMode] = useState<boolean>(false);
  const [rawActiveOrders, setRawActiveOrders] = useState<any[]>([]);
  const [rawHistoryOrders, setRawHistoryOrders] = useState<any[]>([]);

  // 处理API返回的订单数据，调整数据格式以适配新的表格列
  const formatOrderData = (order: any, index: number) => {
    // 计算成交比例
    const filledSize = parseFloat(order.filled_size || '0');
    const totalSize = parseFloat(order.size || '0');
    const filledRatio = totalSize > 0 ? (filledSize / totalSize * 100).toFixed(2) : '0';
    
    // 交易方向格式化
    const direction = order.side === 'buy' ? '买入' : '卖出';
    
    // 优化时间格式处理逻辑
    let formattedTime = '未知时间';
    try {
      // OKCoin API返回的时间字段 created_at 或 timestamp
      // 注意：API返回的时间戳包含2025年（这是API测试环境的特性），但我们仍然正确显示
      const timeValue = order.created_at || order.timestamp;
      if (timeValue) {
        // 直接解析ISO格式的时间字符串，忽略年份，仅显示月日时分秒
        const date = new Date(timeValue);
        if (!isNaN(date.getTime())) {
          // 使用toLocaleString格式化时间，不显示年份
          formattedTime = date.toLocaleString('zh-CN', {
            month: '2-digit',
            day: '2-digit',
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit',
            hour12: false
          });
        } else {
          console.warn('无法解析时间:', timeValue);
        }
      }
    } catch (e) {
      console.error('时间格式转换错误:', e, { created_at: order.created_at, timestamp: order.timestamp });
    }
    
    // 优化委托总量与已成交量处理
    const size = order.size || '0';
    const filledSize2 = order.filled_size || '0';
    
    // 优化价格处理：成交均价和委托价
    let priceDisplay = '市价';
    if (order.price_avg && parseFloat(order.price_avg) > 0) {
      // 有成交均价的情况
      if (order.price && parseFloat(order.price) > 0) {
        // 同时有委托价
        priceDisplay = `${order.price_avg} | ${order.price}`;
      } else {
        // 只有成交均价
        priceDisplay = `${order.price_avg}`;
      }
    } else if (order.price && parseFloat(order.price) > 0) {
      // 只有委托价
      priceDisplay = `${order.price}`;
    } else if (order.type === 'market') {
      // 明确是市价单
      priceDisplay = '市价';
    }
    
    // 优化展示格式
    return {
      key: order.order_id || index.toString(),
      time: formattedTime,
      pair: order.instrument_id ? order.instrument_id.replace('-', '/') : tradingPair,
      direction: direction,
      filledRatio: `${filledRatio}%`,
      amount: `${filledSize2} | ${size}`,
      price: priceDisplay,
      status: getOrderStatus(order.state),
      order_id: order.order_id,
      instrument_id: order.instrument_id,
      // 保存原始数据，用于详细显示
      rawData: order
    };
  };

  // 获取当前委托
  const fetchActiveOrders = useCallback(async () => {
    try {
      setLoadingActive(true);
      setError(null);
      
      const response = await fetch('http://localhost:5001/api/order_list', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ tradingPair }),
      });
      
      if (!response.ok) {
        throw new Error(`HTTP错误: ${response.status}`);
      }
      
      const result = await response.json();
      
      if (result.error) {
        throw new Error(result.error);
      }
      
      // 处理OKCoin API返回的元组格式 [orders, pagination]
      let orders = [];
      if (Array.isArray(result) && result.length > 0) {
        // 检查是否为元组格式（第一个元素是订单数组，第二个元素是分页信息）
        if (Array.isArray(result[0])) {
          setRawActiveOrders(result[0]);
          orders = result[0];
        } else {
          // 直接是订单数组
          setRawActiveOrders(result);
          orders = result;
        }
        
        // 格式化数据以适配表格
        const formattedOrders = orders.map(formatOrderData);
        
        setActiveOrders(formattedOrders);
        setActiveOrdersPaging(prev => ({
          ...prev,
          total: formattedOrders.length
        }));
        setLastRefreshTime(new Date());
      } else {
        // 如果没有数据或格式不正确，设置为空数组
        setRawActiveOrders([]);
        setActiveOrders([]);
        setActiveOrdersPaging(prev => ({
          ...prev,
          total: 0
        }));
      }
    } catch (error: any) {
      console.error('获取当前委托失败:', error);
      setError(`获取当前委托失败: ${error.message}`);
      message.error(`获取当前委托失败: ${error.message}`);
    } finally {
      setLoadingActive(false);
    }
  }, [tradingPair]);

  // 获取历史委托
  const fetchHistoryOrders = useCallback(async () => {
    try {
      setLoadingHistory(true);
      setError(null);
      
      const response = await fetch('http://localhost:5001/api/order_history', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ tradingPair }),
      });
      
      if (!response.ok) {
        throw new Error(`HTTP错误: ${response.status}`);
      }
      
      const result = await response.json();
      
      if (result.error) {
        throw new Error(result.error);
      }
      
      // 处理OKCoin API返回的元组格式 [orders, pagination]
      let orders = [];
      if (Array.isArray(result) && result.length > 0) {
        // 检查是否为元组格式（第一个元素是订单数组，第二个元素是分页信息）
        if (Array.isArray(result[0])) {
          setRawHistoryOrders(result[0]);
          orders = result[0];
        } else {
          // 直接是订单数组
          setRawHistoryOrders(result);
          orders = result;
        }
        
        // 格式化数据以适配表格
        const formattedOrders = orders.map(formatOrderData);
        
        setHistoryOrders(formattedOrders);
        setHistoryOrdersPaging(prev => ({
          ...prev,
          total: formattedOrders.length
        }));
        setLastRefreshTime(new Date());
      } else {
        // 如果没有数据或格式不正确，设置为空数组
        setRawHistoryOrders([]);
        setHistoryOrders([]);
        setHistoryOrdersPaging(prev => ({
          ...prev,
          total: 0
        }));
      }
    } catch (error: any) {
      console.error('获取历史委托失败:', error);
      setError(`获取历史委托失败: ${error.message}`);
      message.error(`获取历史委托失败: ${error.message}`);
    } finally {
      setLoadingHistory(false);
    }
  }, [tradingPair]);

  // 处理订单状态
  const getOrderStatus = (state: string) => {
    const statusMap: {[key: string]: string} = {
      '-2': '已取消',
      '-1': '已撤单',
      '0': '待成交',
      '1': '部分成交',
      '2': '已成交',
      '3': '下单中',
      '4': '撤单中'
    };
    return statusMap[state] || '未知状态';
  };
  
  // 计算成交总额
  const calculateTotal = (order: any) => {
    if (order.price && order.filled_size) {
      return (parseFloat(order.price) * parseFloat(order.filled_size)).toFixed(2);
    }
    return '0';
  };

  // 取消订单
  const cancelOrder = async (orderId: string, instrumentId: string) => {
    try {
      message.info(`正在取消订单: ${orderId}`);
      
      const response = await fetch('http://localhost:5001/api/cancel_order', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          order_id: orderId,
          instrument_id: instrumentId
        }),
      });
      
      if (!response.ok) {
        throw new Error(`HTTP错误: ${response.status}`);
      }
      
      const result = await response.json();
      
      if (result.error) {
        throw new Error(result.error);
      }
      
      message.success('订单已取消');
      
      // 刷新订单列表
      fetchActiveOrders();
    } catch (error: any) {
      message.error(`取消订单失败: ${error.message}`);
      console.error('取消订单失败:', error);
    }
  };

  // 手动刷新函数
  const handleRefresh = () => {
    fetchActiveOrders();
    fetchHistoryOrders();
    message.success('数据已刷新');
  };
  
  // 搜索过滤函数 - 更新搜索字段
  const filterOrders = (orders: any[], searchKey: string) => {
    if (!searchKey) return orders;
    const keyword = searchKey.toLowerCase();
    return orders.filter(order => 
      order.order_id?.toLowerCase().includes(keyword) ||
      order.pair?.toLowerCase().includes(keyword) ||
      order.direction?.toLowerCase().includes(keyword) ||
      order.status?.toLowerCase().includes(keyword) ||
      order.price?.toString().includes(keyword)
    );
  };
  
  // 分页变化处理函数
  const handleActivePageChange = (page: number, pageSize: number) => {
    setActiveOrdersPaging({
      current: page,
      pageSize: pageSize,
      total: activeOrders.length
    });
  };
  
  const handleHistoryPageChange = (page: number, pageSize: number) => {
    setHistoryOrdersPaging({
      current: page,
      pageSize: pageSize,
      total: historyOrders.length
    });
  };

  // 设置自动刷新
  useEffect(() => {
    if (autoRefresh) {
      // 清除旧定时器
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
      }
      
      // 设置新定时器
      intervalRef.current = setInterval(() => {
        fetchActiveOrders();
        fetchHistoryOrders();
      }, refreshInterval * 1000);
      
      // 返回清理函数，组件卸载时清除定时器
      return () => {
        if (intervalRef.current) {
          clearInterval(intervalRef.current);
        }
      };
    } else if (intervalRef.current) {
      // 如果关闭自动刷新，清除定时器
      clearInterval(intervalRef.current);
    }
  }, [autoRefresh, refreshInterval, fetchActiveOrders, fetchHistoryOrders]);

  // 当交易对变化时刷新数据
  useEffect(() => {
    fetchActiveOrders();
    fetchHistoryOrders();
  }, [tradingPair, fetchActiveOrders, fetchHistoryOrders]);

  const activeColumns = [
    {
      title: '委托时间',
      dataIndex: 'time',
      key: 'time',
    },
    {
      title: '币对',
      dataIndex: 'pair',
      key: 'pair',
    },
    {
      title: '交易方向',
      dataIndex: 'direction',
      key: 'direction',
      render: (direction: string) => {
        const color = direction === '买入' ? 'green' : 'red';
        return <Tag color={color}>{direction}</Tag>;
      },
    },
    {
      title: '成交比例',
      dataIndex: 'filledRatio',
      key: 'filledRatio',
    },
    {
      title: '已成交量 | 委托总量',
      dataIndex: 'amount',
      key: 'amount',
    },
    {
      title: '成交均价 | 委托价',
      dataIndex: 'price',
      key: 'price',
    },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
      render: (status: string) => {
        const color = status === '待成交' ? 'orange' : 
                     status === '部分成交' ? 'blue' : 
                     status === '已成交' ? 'green' : 'red';
        return <Tag color={color}>{status}</Tag>;
      },
    },
    {
      title: '操作',
      key: 'action',
      render: (text: string, record: any) => (
        <a onClick={() => cancelOrder(record.order_id, record.instrument_id)}>取消</a>
      ),
    },
  ];

  const historyColumns = [
    ...activeColumns,
    {
      title: '成交金额',
      dataIndex: 'totalAmount',
      key: 'totalAmount',
      render: (_: any, record: any) => {
        // 改进成交金额计算逻辑
        // 优先使用原始数据中的filled_notional字段（成交金额）
        if (record.rawData && record.rawData.filled_notional) {
          return `${parseFloat(record.rawData.filled_notional).toFixed(2)} JPY`;
        }
        
        // 如果没有filled_notional字段，则计算 成交均价 * 成交数量
        let price = 0;
        let amount = 0;
        
        // 获取价格（优先使用成交均价price_avg）
        if (record.rawData && record.rawData.price_avg && parseFloat(record.rawData.price_avg) > 0) {
          price = parseFloat(record.rawData.price_avg);
        } else if (record.price) {
          // 从显示字符串中提取价格
          const priceString = record.price;
          const priceMatch = priceString.match(/(\d+(\.\d+)?)/);
          price = priceMatch ? parseFloat(priceMatch[0]) : 0;
        }
        
        // 获取成交数量（优先使用filled_size）
        if (record.rawData && record.rawData.filled_size) {
          amount = parseFloat(record.rawData.filled_size);
        } else if (record.amount) {
          // 从显示字符串中提取已成交数量
          const amountString = record.amount;
          const amountParts = amountString.split('|');
          if (amountParts.length > 0) {
            const filledAmount = amountParts[0].trim();
            amount = parseFloat(filledAmount);
          }
        }
        
        const total = (price * amount).toFixed(2);
        return `${total} JPY`;
      }
    },
    {
      title: '手续费',
      dataIndex: 'fee',
      key: 'fee',
      render: (_: any, record: any) => {
        // 改进手续费显示逻辑
        if (record.rawData && record.rawData.fee) {
          // 添加手续费币种
          const feeCurrency = record.rawData.fee_currency || '';
          return `${record.rawData.fee} ${feeCurrency}`;
        }
        return '0';
      }
    },
  ];

  // 获取筛选后的数据
  const filteredActiveOrders = filterOrders(activeOrders, searchText);
  const filteredHistoryOrders = filterOrders(historyOrders, searchText);

  return (
    <OrderListContainer>
      <ControlBar>
        <SearchContainer>
          <Input
            placeholder="搜索订单ID/交易对/状态"
            prefix={<SearchOutlined />}
            value={searchText}
            onChange={e => setSearchText(e.target.value)}
            style={{ width: 220 }}
            allowClear
          />
        </SearchContainer>
        <RefreshContainer>
          <Space>
            <span>自动刷新: </span>
            <Switch checked={autoRefresh} onChange={setAutoRefresh} />
            <Tooltip title="立即刷新">
              <Button 
                icon={<ReloadOutlined />} 
                onClick={handleRefresh}
                loading={loadingActive || loadingHistory}
              />
            </Tooltip>
            <Badge status="processing" text={`上次刷新: ${lastRefreshTime.toLocaleTimeString()}`} />
            <Tooltip title="开发者模式">
              <Switch
                checkedChildren="调试开"
                unCheckedChildren="调试关"
                checked={debugMode}
                onChange={setDebugMode}
              />
            </Tooltip>
          </Space>
        </RefreshContainer>
      </ControlBar>
      <Tabs defaultActiveKey="active">
        <TabPane tab={`当前委托 (${filteredActiveOrders.length})`} key="active">
          {loadingActive ? (
            <div style={{ textAlign: 'center', padding: '20px' }}>
              <Spin tip="加载中..." />
            </div>
          ) : filteredActiveOrders.length > 0 ? (
            <Table 
              columns={activeColumns} 
              dataSource={filteredActiveOrders}
              pagination={{
                current: activeOrdersPaging.current,
                pageSize: activeOrdersPaging.pageSize,
                total: filteredActiveOrders.length,
                onChange: handleActivePageChange,
                showSizeChanger: true,
                showQuickJumper: true,
                showTotal: (total) => `共 ${total} 条订单`
              }}
            />
          ) : (
            <div style={{ textAlign: 'center', padding: '20px', color: '#999' }}>
              {error ? error : searchText ? '没有找到匹配的订单' : '暂无当前委托'}
            </div>
          )}
          
          {/* 调试模式下显示原始数据 */}
          {debugMode && rawActiveOrders.length > 0 && (
            <DebugContainer>
              <div style={{ marginBottom: '10px', fontWeight: 'bold' }}>当前委托原始数据：</div>
              {JSON.stringify(rawActiveOrders, null, 2)}
            </DebugContainer>
          )}
        </TabPane>
        <TabPane tab={`历史委托 (${filteredHistoryOrders.length})`} key="history">
          {loadingHistory ? (
            <div style={{ textAlign: 'center', padding: '20px' }}>
              <Spin tip="加载中..." />
            </div>
          ) : filteredHistoryOrders.length > 0 ? (
            <Table 
              columns={historyColumns} 
              dataSource={filteredHistoryOrders}
              pagination={{
                current: historyOrdersPaging.current,
                pageSize: historyOrdersPaging.pageSize,
                total: filteredHistoryOrders.length,
                onChange: handleHistoryPageChange,
                showSizeChanger: true,
                showQuickJumper: true,
                showTotal: (total) => `共 ${total} 条订单`
              }}
            />
          ) : (
            <div style={{ textAlign: 'center', padding: '20px', color: '#999' }}>
              {error ? error : searchText ? '没有找到匹配的订单' : '暂无历史委托'}
            </div>
          )}
          
          {/* 调试模式下显示原始数据 */}
          {debugMode && rawHistoryOrders.length > 0 && (
            <DebugContainer>
              <div style={{ marginBottom: '10px', fontWeight: 'bold' }}>历史委托原始数据：</div>
              {JSON.stringify(rawHistoryOrders, null, 2)}
            </DebugContainer>
          )}
        </TabPane>
      </Tabs>
    </OrderListContainer>
  );
};

export default OrderList; 