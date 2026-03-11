//
//  ContentView.swift
//  OK_IOS_PM
//
//  Created by mc on 2025/5/19.
//
import SwiftUI

struct ContentView: View {
    @State private var selectedTab = 2
    
    var body: some View {
        TabView(selection: $selectedTab) {
            Text("欧易")
                .tabItem {
                    Image(systemName: "house")
                    Text("欧易")
                }
                .tag(0)
            
            Text("行情")
                .tabItem {
                    Image(systemName: "chart.xyaxis.line")
                    Text("行情")
                }
                .tag(1)
            
            StrategyTradingView()
                .tabItem {
                    Image(systemName: "arrow.left.arrow.right")
                    Text("交易")
                }
                .tag(2)
            
            Text("探索")
                .tabItem {
                    Image(systemName: "magnifyingglass")
                    Text("探索")
                }
                .tag(3)
            
            Text("资产")
                .tabItem {
                    Image(systemName: "wallet.pass")
                    Text("资产")
                }
                .tag(4)
        }
        .accentColor(.black)
    }
}

struct StrategyTradingView: View {
    @State private var isSpotGridViewPresented = false
    
    var body: some View {
        NavigationView {
            VStack(alignment: .leading, spacing: 0) {
                // 顶部标题和操作按钮
                HStack {
                    Text("策略交易")
                        .font(.title2)
                        .fontWeight(.bold)
                    
                    Spacer()
                    
                    Button(action: {}) {
                        Image(systemName: "book")
                            .font(.title2)
                    }
                    
                    Button(action: {}) {
                        Image(systemName: "ellipsis")
                            .font(.title2)
                            .padding(.leading, 16)
                    }
                }
                .padding(.horizontal)
                .padding(.top, 8)
                
                // 总资产信息
                VStack(alignment: .leading, spacing: 4) {
                    HStack {
                        Text("总资产估值")
                            .font(.subheadline)
                            .foregroundColor(.secondary)
                        
                        Image(systemName: "eye")
                            .foregroundColor(.secondary)
                    }
                    
                    HStack {
                        Text("0.00")
                            .font(.system(size: 32, weight: .bold))
                        
                        Text("USD")
                            .fontWeight(.medium)
                        
                        Image(systemName: "chevron.right")
                    }
                    
                    HStack {
                        Text("0 (0.00%)")
                            .font(.subheadline)
                            .foregroundColor(.secondary)
                        
                        Text("今日收益")
                            .font(.subheadline)
                            .foregroundColor(.secondary)
                    }
                }
                .padding(.horizontal)
                .padding(.top, 16)
                
                // 创建策略提示卡片
                HStack {
                    VStack(alignment: .leading, spacing: 8) {
                        Text("点击前往策略精选页面，探索更多的优质策略。")
                            .font(.subheadline)
                            .foregroundColor(.secondary)
                        
                        HStack {
                            Circle()
                                .fill(Color.secondary)
                                .frame(width: 6, height: 6)
                            Circle()
                                .fill(Color.secondary.opacity(0.5))
                                .frame(width: 6, height: 6)
                        }
                    }
                    .padding(.vertical, 16)
                    
                    Spacer()
                    
                    Image(systemName: "dollarsign.square.fill")
                        .resizable()
                        .frame(width: 40, height: 40)
                        .foregroundColor(.secondary)
                }
                .padding(.horizontal)
                .padding(.vertical, 8)
                .background(Color(UIColor.systemGray6))
                .cornerRadius(12)
                .padding(.horizontal)
                .padding(.top, 16)
                
                // 推荐和运行中标签
                HStack(spacing: 20) {
                    Text("推荐")
                        .fontWeight(.medium)
                        .padding(.vertical, 12)
                        .overlay(
                            Rectangle()
                                .frame(height: 2)
                                .foregroundColor(.black),
                            alignment: .bottom
                        )
                    
                    Text("运行中 (0)")
                        .foregroundColor(.secondary)
                }
                .padding(.horizontal)
                .padding(.top, 16)
                
                // 策略类型按钮
                ScrollView(.horizontal, showsIndicators: false) {
                    HStack(spacing: 20) {
                        // 创建策略按钮
                        VStack {
                            ZStack {
                                Circle()
                                    .fill(Color.black)
                                    .frame(width: 60, height: 60)
                                
                                Image(systemName: "plus")
                                    .resizable()
                                    .frame(width: 20, height: 20)
                                    .foregroundColor(.white)
                            }
                            
                            Text("创建策略")
                                .font(.caption)
                                .padding(.top, 4)
                        }
                        
                        // 现货网格按钮
                        NavigationLink(destination: SpotGridView(), isActive: $isSpotGridViewPresented) {
                            Button(action: {
                                isSpotGridViewPresented = true
                            }) {
                                VStack {
                                    ZStack {
                                        Circle()
                                            .fill(Color(UIColor.systemGray6))
                                            .frame(width: 60, height: 60)
                                        
                                        Image(systemName: "chart.bar.fill")
                                            .resizable()
                                            .frame(width: 24, height: 20)
                                            .foregroundColor(.black)
                                    }
                                    
                                    Text("现货网格")
                                        .font(.caption)
                                        .padding(.top, 4)
                                }
                            }
                            .buttonStyle(PlainButtonStyle())
                        }
                        
                        // 合约网格按钮
                        VStack {
                            ZStack {
                                Circle()
                                    .fill(Color(UIColor.systemGray6))
                                    .frame(width: 60, height: 60)
                                
                                Image(systemName: "chart.xyaxis.line")
                                    .resizable()
                                    .frame(width: 24, height: 20)
                                    .foregroundColor(.black)
                            }
                            
                            Text("合约网格")
                                .font(.caption)
                                .padding(.top, 4)
                        }
                        
                        // 智能套利按钮
                        VStack {
                            ZStack {
                                Circle()
                                    .fill(Color(UIColor.systemGray6))
                                    .frame(width: 60, height: 60)
                                
                                Image(systemName: "arrow.triangle.2.circlepath")
                                    .resizable()
                                    .frame(width: 24, height: 20)
                                    .foregroundColor(.black)
                            }
                            
                            Text("智能套利")
                                .font(.caption)
                                .padding(.top, 4)
                        }
                    }
                    .padding(.horizontal)
                    .padding(.top, 16)
                }
                
                // 热门策略标题
                Text("热门策略")
                    .font(.headline)
                    .fontWeight(.bold)
                    .padding(.horizontal)
                    .padding(.top, 20)
                
                // 热门策略列表
                ScrollView {
                    VStack(spacing: 0) {
                        // 抄底止盈策略
                        HStack {
                            ZStack {
                                Circle()
                                    .fill(Color(UIColor.systemGray6))
                                    .frame(width: 50, height: 50)
                                
                                Image(systemName: "arrow.up.arrow.down")
                                    .resizable()
                                    .frame(width: 20, height: 20)
                                    .foregroundColor(.black)
                            }
                            
                            VStack(alignment: .leading) {
                                Text("抄底止盈策略")
                                    .fontWeight(.medium)
                                
                                Text("双币理财，买低卖高，循环套利")
                                    .font(.caption)
                                    .foregroundColor(.secondary)
                            }
                            .padding(.leading, 8)
                            
                            Spacer()
                            
                            Image(systemName: "chevron.right")
                                .foregroundColor(.secondary)
                        }
                        .padding(.vertical, 12)
                        .padding(.horizontal)
                        
                        Divider()
                        
                        // 合约马丁格尔
                        HStack {
                            ZStack {
                                Circle()
                                    .fill(Color(UIColor.systemGray6))
                                    .frame(width: 50, height: 50)
                                
                                Image(systemName: "dollarsign.square.fill")
                                    .resizable()
                                    .frame(width: 20, height: 20)
                                    .foregroundColor(.black)
                            }
                            
                            VStack(alignment: .leading) {
                                Text("合约马丁格尔")
                                    .fontWeight(.medium)
                                
                                Text("高抛低吸，分批进场")
                                    .font(.caption)
                                    .foregroundColor(.secondary)
                            }
                            .padding(.leading, 8)
                            
                            Spacer()
                            
                            Image(systemName: "chevron.right")
                                .foregroundColor(.secondary)
                        }
                        .padding(.vertical, 12)
                        .padding(.horizontal)
                        
                        Divider()
                        
                        // 现货马丁格尔
                        HStack {
                            ZStack {
                                Circle()
                                    .fill(Color(UIColor.systemGray6))
                                    .frame(width: 50, height: 50)
                                
                                Image(systemName: "arrow.2.circlepath")
                                    .resizable()
                                    .frame(width: 20, height: 20)
                                    .foregroundColor(.black)
                            }
                            
                            VStack(alignment: .leading) {
                                Text("现货马丁格尔")
                                    .fontWeight(.medium)
                                
                                Text("信号触发，分批加仓")
                                    .font(.caption)
                                    .foregroundColor(.secondary)
                            }
                            .padding(.leading, 8)
                            
                            Spacer()
                            
                            Image(systemName: "chevron.right")
                                .foregroundColor(.secondary)
                        }
                        .padding(.vertical, 12)
                        .padding(.horizontal)
                        
                        Divider()
                        
                        // 信号策略
                        HStack {
                            ZStack {
                                Circle()
                                    .fill(Color(UIColor.systemGray6))
                                    .frame(width: 50, height: 50)
                                
                                Image(systemName: "bell.fill")
                                    .resizable()
                                    .frame(width: 20, height: 20)
                                    .foregroundColor(.black)
                            }
                            
                            VStack(alignment: .leading) {
                                Text("信号策略")
                                    .fontWeight(.medium)
                                
                                Text("全自动交易，高可靠低时延")
                                    .font(.caption)
                                    .foregroundColor(.secondary)
                            }
                            .padding(.leading, 8)
                            
                            Spacer()
                            
                            Image(systemName: "chevron.right")
                                .foregroundColor(.secondary)
                        }
                        .padding(.vertical, 12)
                        .padding(.horizontal)
                        
                        // 底部推荐信息
                        HStack {
                            Text("策略交易新人？ 不妨试试平台热门精选，助您轻松赚钱！ →")
                                .font(.subheadline)
                            
                            Spacer()
                        }
                        .padding()
                        .background(Color(UIColor.systemGray6))
                        .padding(.top, 16)
                    }
                }
            }
            .navigationBarHidden(true)
        }
    }
}

struct SpotGridView: View {
    @Environment(\.presentationMode) var presentationMode
    @State private var selectedTimeframe = "1分"
    let timeframeOptions = ["15分", "1时", "4时", "1日", "1分"]
    
    var body: some View {
        VStack(spacing: 0) {
            // 顶部导航栏
            HStack {
                Button(action: {
                    presentationMode.wrappedValue.dismiss()
                }) {
                    Image(systemName: "chevron.left")
                        .font(.title3)
                        .foregroundColor(.black)
                }
                
                Spacer()
                
                Text("现货网格")
                    .font(.headline)
                    .fontWeight(.medium)
                
                Image(systemName: "chevron.down")
                    .font(.caption)
                
                Spacer()
                
                HStack(spacing: 16) {
                    Button(action: {}) {
                        Image(systemName: "book")
                            .font(.title3)
                            .foregroundColor(.black)
                    }
                    
                    Button(action: {}) {
                        Image(systemName: "ellipsis")
                            .font(.title3)
                            .foregroundColor(.black)
                    }
                }
            }
            .padding(.horizontal)
            .padding(.top, 8)
            .padding(.bottom, 12)
            
            // BTC/USDT 标题和价格
            HStack {
                Text("BTC/USDT")
                    .font(.headline)
                    .fontWeight(.medium)
                
                Image(systemName: "chevron.down")
                    .font(.caption)
                
                Spacer()
                
                Text("103,873.9")
                    .font(.headline)
                    .foregroundColor(.green)
                
                Image(systemName: "arrow.up")
                    .font(.caption)
                    .foregroundColor(.green)
                
                Button(action: {}) {
                    Image(systemName: "arrow.left.arrow.right")
                        .foregroundColor(.black)
                }
                
                Button(action: {}) {
                    Image(systemName: "chevron.up")
                        .foregroundColor(.black)
                }
            }
            .padding(.horizontal)
            
            // 图表时间选择
            HStack {
                ScrollView(.horizontal, showsIndicators: false) {
                    HStack(spacing: 24) {
                        ForEach(timeframeOptions, id: \.self) { option in
                            Text(option)
                                .font(.subheadline)
                                .foregroundColor(option == selectedTimeframe ? .black : .secondary)
                                .fontWeight(option == selectedTimeframe ? .medium : .regular)
                        }
                    }
                    .padding(.horizontal)
                }
            }
            .padding(.top, 8)
            
            // K线图(模拟)
            ZStack {
                // 简单模拟K线图
                VStack {
                    HStack(alignment: .bottom, spacing: 2) {
                        ForEach(0..<20) { i in
                            let height = Double.random(in: 40...120)
                            let isGreen = Bool.random()
                            
                            Rectangle()
                                .fill(isGreen ? Color.green : Color.red)
                                .frame(width: 10, height: height)
                        }
                    }
                    .frame(height: 150, alignment: .center)
                    
                    // MA指标信息
                    HStack {
                        Text("MA5: 103,864.4")
                            .font(.caption)
                            .foregroundColor(.yellow)
                        
                        Text("MA10: 103,881.4")
                            .font(.caption)
                            .foregroundColor(.red)
                        
                        Text("MA20: 103,910.4")
                            .font(.caption)
                            .foregroundColor(.blue)
                    }
                    .frame(maxWidth: .infinity, alignment: .leading)
                    .padding(.horizontal)
                    .padding(.top, 4)
                }
                
                // 价格标签
                HStack {
                    VStack {
                        Text("104,080.0")
                            .font(.caption)
                            .foregroundColor(.secondary)
                            .frame(maxWidth: .infinity, alignment: .trailing)
                        
                        Spacer()
                        
                        Text("104,000.0")
                            .font(.caption)
                            .foregroundColor(.secondary)
                            .frame(maxWidth: .infinity, alignment: .trailing)
                        
                        Spacer()
                        
                        Text("103,920.0")
                            .font(.caption)
                            .foregroundColor(.secondary)
                            .frame(maxWidth: .infinity, alignment: .trailing)
                        
                        Spacer()
                        
                        Text("103,873.9")
                            .font(.caption)
                            .foregroundColor(.secondary)
                            .padding(4)
                            .background(Color.white)
                            .cornerRadius(4)
                            .overlay(
                                RoundedRectangle(cornerRadius: 4)
                                    .stroke(Color.gray, lineWidth: 0.5)
                            )
                            .frame(maxWidth: .infinity, alignment: .trailing)
                    }
                    .frame(width: 80)
                }
                .padding(.trailing)
            }
            .frame(height: 200)
            .padding(.top, 8)
            
            // AI策略和手动创建按钮
            HStack(spacing: 16) {
                Button(action: {}) {
                    HStack {
                        Spacer()
                        Text("AI 策略")
                            .foregroundColor(.black)
                            .fontWeight(.medium)
                        Spacer()
                    }
                    .padding(.vertical, 12)
                    .background(Color(UIColor.systemGray6))
                    .cornerRadius(8)
                }
                
                Button(action: {}) {
                    HStack {
                        Spacer()
                        Text("手动创建")
                            .foregroundColor(.black)
                            .fontWeight(.medium)
                        Spacer()
                    }
                    .padding(.vertical, 12)
                    .background(Color(UIColor.systemGray6))
                    .cornerRadius(8)
                }
            }
            .padding(.horizontal)
            .padding(.top, 16)
            
            // 参数设置区域
            ScrollView {
                VStack(alignment: .leading, spacing: 24) {
                    // 价格区间设置
                    HStack {
                        Text("价格区间 (USDT)")
                            .font(.subheadline)
                        
                        Spacer()
                        
                        Button(action: {}) {
                            Image(systemName: "square.and.pencil")
                                .foregroundColor(.black)
                        }
                    }
                    
                    // 最低价-最高价输入区域
                    HStack {
                        TextField("最低价", text: .constant(""))
                            .padding()
                            .background(Color(UIColor.systemGray6))
                            .cornerRadius(8)
                        
                        Text("-")
                            .padding(.horizontal, 8)
                        
                        TextField("最高价", text: .constant(""))
                            .padding()
                            .background(Color(UIColor.systemGray6))
                            .cornerRadius(8)
                    }
                    
                    // 网格数量设置
                    VStack(alignment: .leading, spacing: 8) {
                        HStack {
                            Text("网格数量 (2 - 500)")
                                .font(.subheadline)
                            
                            Image(systemName: "info.circle")
                                .foregroundColor(.secondary)
                                .font(.caption)
                            
                            Spacer()
                        }
                        
                        // 网格数量滑块
                        ZStack(alignment: .leading) {
                            Rectangle()
                                .fill(Color(UIColor.systemGray5))
                                .frame(height: 40)
                                .cornerRadius(8)
                            
                            Text("2 ~ 500")
                                .foregroundColor(.secondary)
                                .padding(.leading)
                        }
                    }
                    
                    // 单向网格收益率
                    HStack {
                        Text("单向网格收益率")
                            .font(.subheadline)
                        
                        Spacer()
                        
                        Text("--")
                            .foregroundColor(.secondary)
                    }
                    
                    // 投资额设置
                    VStack(alignment: .leading, spacing: 8) {
                        Text("投资额")
                            .font(.subheadline)
                        
                        HStack {
                            ZStack(alignment: .leading) {
                                Rectangle()
                                    .fill(Color(UIColor.systemGray5))
                                    .frame(height: 40)
                                    .cornerRadius(8)
                                
                                HStack {
                                    Text("> 0")
                                        .foregroundColor(.black)
                                        .padding(.leading)
                                    
                                    Spacer()
                                    
                                    Text("USDT")
                                        .foregroundColor(.black)
                                        .padding(.trailing)
                                }
                            }
                        }
                        
                        // 滑块
                        HStack {
                            ForEach(0..<5) { _ in
                                Circle()
                                    .fill(Color.gray.opacity(0.3))
                                    .frame(width: 8, height: 8)
                                
                                Spacer()
                            }
                        }
                        .padding(.horizontal, 4)
                        .padding(.top, 8)
                        
                        HStack {
                            Text("可用")
                                .font(.caption)
                                .foregroundColor(.secondary)
                            
                            Spacer()
                            
                            Text("0 USDT")
                                .font(.caption)
                            
                            Button(action: {}) {
                                Image(systemName: "plus.circle")
                                    .foregroundColor(.black)
                            }
                        }
                        .padding(.top, 4)
                    }
                    
                    // 高级设置
                    HStack {
                        Text("高级设置")
                            .font(.subheadline)
                        
                        Image(systemName: "info.circle")
                            .foregroundColor(.secondary)
                            .font(.caption)
                        
                        Spacer()
                        
                        Image(systemName: "chevron.down")
                            .foregroundColor(.black)
                    }
                }
                .padding(.horizontal)
                .padding(.top, 16)
            }
            
            Spacer()
            
            // 创建策略按钮
            Button(action: {}) {
                Text("创建策略")
                    .foregroundColor(.white)
                    .fontWeight(.medium)
                    .frame(maxWidth: .infinity)
                    .padding(.vertical, 16)
                    .background(Color.black)
                    .cornerRadius(30)
                    .padding(.horizontal)
                    .padding(.bottom, 16)
            }
        }
        .navigationBarHidden(true)
    }
}

#Preview {
    ContentView()
}
