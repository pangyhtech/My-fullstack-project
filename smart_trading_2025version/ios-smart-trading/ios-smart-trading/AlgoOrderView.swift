import SwiftUI

struct AlgoOrderView: View {
    @State private var selectedTradeType = 0 // 0: 买入, 1: 卖出
    @State private var amount: String = ""
    @State private var selectedCurrency = 0 // 0: BTC, 1: USDT
    @State private var selectedStrategy = 0 // 0: TWAP, 1: POV
    @State private var hours: String = "1"
    @State private var minutes: String = ""
    @State private var selectedTimeDuration = 1 // 预设的时间按钮
    @State private var delayStartTime: String = ""
    @State private var limitPrice: String = ""
    
    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 20) {
                // 交易对展示
                HStack {
                    Text("BTCUSDT")
                        .font(.title2)
                        .fontWeight(.bold)
                        .foregroundColor(.white)
                    
                    Image(systemName: "chevron.down")
                        .foregroundColor(.gray)
                    
                    Spacer()
                    
                    HStack(spacing: 5) {
                        Text("104,207.73")
                            .font(.title2)
                            .fontWeight(.bold)
                            .foregroundColor(.white)
                        
                        VStack(alignment: .leading) {
                            Text("24H")
                                .font(.system(size: 12))
                                .foregroundColor(.gray)
                            
                            Text("+0.90%")
                                .font(.system(size: 12))
                                .foregroundColor(.green)
                        }
                    }
                }
                .padding(.bottom, 10)
                
                // 买入/卖出切换
                HStack(spacing: 0) {
                    tradeTypeButton(title: "买入BTC", isSelected: selectedTradeType == 0) {
                        selectedTradeType = 0
                    }
                    
                    tradeTypeButton(title: "卖出BTC", isSelected: selectedTradeType == 1) {
                        selectedTradeType = 1
                    }
                }
                .background(Color(hex: "171B26"))
                .cornerRadius(4)
                
                // 数量输入
                VStack(alignment: .leading, spacing: 10) {
                    Text("数量(BTC)")
                        .font(.system(size: 14))
                        .foregroundColor(.gray)
                    
                    HStack(spacing: 0) {
                        TextField("0.00", text: $amount)
                            .keyboardType(.decimalPad)
                            .padding()
                            .background(Color(hex: "171B26"))
                            .foregroundColor(.white)
                            .cornerRadius(4)
                        
                        HStack(spacing: 0) {
                            Button(action: {
                                selectedCurrency = 0
                            }) {
                                Text("BTC")
                                    .font(.system(size: 14))
                                    .foregroundColor(selectedCurrency == 0 ? .black : .white)
                                    .padding(.vertical, 8)
                                    .padding(.horizontal, 12)
                                    .background(selectedCurrency == 0 ? Color.yellow : Color.clear)
                                    .cornerRadius(4)
                            }
                            
                            Button(action: {
                                selectedCurrency = 1
                            }) {
                                Text("USDT")
                                    .font(.system(size: 14))
                                    .foregroundColor(selectedCurrency == 1 ? .black : .white)
                                    .padding(.vertical, 8)
                                    .padding(.horizontal, 12)
                                    .background(selectedCurrency == 1 ? Color.yellow : Color.clear)
                                    .cornerRadius(4)
                            }
                        }
                        .background(Color(hex: "171B26"))
                        .cornerRadius(4)
                        .padding(.leading, 5)
                    }
                    
                    Text("≈ 0.00 USDT")
                        .font(.system(size: 14))
                        .foregroundColor(.gray)
                        .padding(.top, -5)
                }
                
                // 执行策略
                VStack(alignment: .leading, spacing: 10) {
                    HStack {
                        Text("执行策略")
                            .font(.headline)
                            .foregroundColor(.white)
                        
                        Image(systemName: "info.circle")
                            .foregroundColor(.gray)
                            .font(.system(size: 14))
                            .padding(.leading, 5)
                        
                        Spacer()
                    }
                    
                    HStack(spacing: 0) {
                        Button(action: {
                            selectedStrategy = 0
                        }) {
                            Text("TWAP")
                                .font(.system(size: 14))
                                .foregroundColor(selectedStrategy == 0 ? .black : .white)
                                .padding(.vertical, 8)
                                .padding(.horizontal, 12)
                                .background(selectedStrategy == 0 ? Color.yellow : Color.clear)
                                .cornerRadius(selectedStrategy == 0 ? 4 : 0)
                        }
                        
                        Button(action: {
                            selectedStrategy = 1
                        }) {
                            Text("POV")
                                .font(.system(size: 14))
                                .foregroundColor(selectedStrategy == 1 ? .black : .white)
                                .padding(.vertical, 8)
                                .padding(.horizontal, 12)
                                .background(selectedStrategy == 1 ? Color.yellow : Color.clear)
                                .cornerRadius(selectedStrategy == 1 ? 4 : 0)
                        }
                    }
                    .background(Color(hex: "171B26"))
                    .cornerRadius(4)
                }
                
                // 建议持续时间
                VStack(alignment: .leading, spacing: 10) {
                    HStack {
                        Text("建议持续时间")
                            .font(.headline)
                            .foregroundColor(.white)
                        
                        Image(systemName: "info.circle")
                            .foregroundColor(.gray)
                            .font(.system(size: 14))
                            .padding(.leading, 5)
                        
                        Spacer()
                        
                        Text("--")
                            .font(.system(size: 14))
                            .foregroundColor(.gray)
                    }
                    
                    // 时长输入
                    HStack(spacing: 10) {
                        HStack(spacing: 5) {
                            TextField("1", text: $hours)
                                .keyboardType(.numberPad)
                                .frame(width: 50)
                                .padding(10)
                                .background(Color(hex: "171B26"))
                                .foregroundColor(.white)
                                .multilineTextAlignment(.center)
                            
                            Text("-168")
                                .foregroundColor(.gray)
                                .font(.system(size: 14))
                            
                            Text("小时")
                                .foregroundColor(.white)
                                .font(.system(size: 14))
                        }
                        
                        HStack(spacing: 5) {
                            TextField("", text: $minutes)
                                .keyboardType(.numberPad)
                                .frame(width: 50)
                                .padding(10)
                                .background(Color(hex: "171B26"))
                                .foregroundColor(.white)
                                .multilineTextAlignment(.center)
                            
                            Text("1-59")
                                .foregroundColor(.gray)
                                .font(.system(size: 14))
                            
                            Text("分钟")
                                .foregroundColor(.white)
                                .font(.system(size: 14))
                        }
                    }
                    
                    HStack {
                        Text("时长")
                            .foregroundColor(.white)
                            .font(.system(size: 14))
                        
                        Image(systemName: "info.circle")
                            .foregroundColor(.gray)
                            .font(.system(size: 12))
                        
                        Spacer()
                    }
                    
                    // 预设时间选项
                    HStack(spacing: 10) {
                        timeButton(title: "30分钟", index: 0)
                        timeButton(title: "1小时", index: 1)
                        timeButton(title: "6小时", index: 2)
                        timeButton(title: "12小时", index: 3)
                    }
                    
                    // 延迟开始时间
                    optionalField(title: "延迟开始时间", text: $delayStartTime)
                    
                    // 限价
                    optionalField(title: "限价(USDT)", text: $limitPrice)
                    
                    // 下单按钮
                    Button(action: {
                        // 下单逻辑
                    }) {
                        Text("下单")
                            .font(.headline)
                            .foregroundColor(.black)
                            .frame(maxWidth: .infinity)
                            .padding()
                            .background(Color.yellow)
                            .cornerRadius(4)
                    }
                    .padding(.top)
                }
            }
            .padding()
        }
        .background(Color(hex: "0D1119"))
    }
    
    // 买入/卖出按钮
    private func tradeTypeButton(title: String, isSelected: Bool, action: @escaping () -> Void) -> some View {
        Button(action: action) {
            Text(title)
                .font(.system(size: 16))
                .foregroundColor(isSelected ? .white : .gray)
                .frame(maxWidth: .infinity)
                .padding(.vertical, 10)
        }
        .background(isSelected ? Color(hex: "242832") : Color.clear)
    }
    
    // 时间选择按钮
    private func timeButton(title: String, index: Int) -> some View {
        Button(action: {
            selectedTimeDuration = index
            switch index {
            case 0:
                hours = "0"
                minutes = "30"
            case 1:
                hours = "1"
                minutes = "0"
            case 2:
                hours = "6"
                minutes = "0"
            case 3:
                hours = "12"
                minutes = "0"
            default:
                break
            }
        }) {
            Text(title)
                .font(.system(size: 14))
                .foregroundColor(selectedTimeDuration == index ? .black : .white)
                .padding(.vertical, 8)
                .padding(.horizontal, 10)
                .frame(maxWidth: .infinity)
                .background(selectedTimeDuration == index ? Color.yellow : Color(hex: "242832"))
                .cornerRadius(4)
        }
    }
    
    // 可选输入字段
    private func optionalField(title: String, text: Binding<String>) -> some View {
        HStack {
            Text("可选")
                .font(.system(size: 14))
                .foregroundColor(.gray)
                .frame(width: 70, alignment: .leading)
            
            Spacer()
            
            Text(title)
                .font(.system(size: 14))
                .foregroundColor(.gray)
        }
        .padding(.vertical, 15)
        .padding(.horizontal)
        .background(Color(hex: "171B26"))
        .cornerRadius(4)
    }
}

struct AlgoOrderView_Previews: PreviewProvider {
    static var previews: some View {
        AlgoOrderView()
    }
} 