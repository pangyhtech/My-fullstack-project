import SwiftUI

struct SpotGridView: View {
    @State private var lowerPrice: String = ""
    @State private var upperPrice: String = ""
    @State private var gridCount: String = "2-170"
    @State private var investment: String = ""
    @State private var gridMode = 0
    @State private var isTrailingUp = false
    @State private var isGridTrigger = false
    @State private var isTPSL = false
    @State private var isSellAllOnStop = true
    
    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 20) {
                // AI/Manual切换
                HStack(spacing: 0) {
                    strategyButton(title: "AI", isSelected: false)
                    strategyButton(title: "Popular", isSelected: false)
                    strategyButton(title: "Manual", isSelected: true)
                }
                .background(Color(hex: "171B26"))
                .cornerRadius(4)
                .padding(.top, 5)
                .padding(.bottom, 10)
                
                // 1. 价格范围
                sectionHeader(title: "1. 价格范围", trailingText: "Auto Fill")
                
                HStack(spacing: 10) {
                    TextField("Lower", text: $lowerPrice)
                        .keyboardType(.decimalPad)
                        .padding()
                        .background(Color(hex: "171B26"))
                        .foregroundColor(.white)
                        .cornerRadius(4)
                    
                    TextField("Upper", text: $upperPrice)
                        .keyboardType(.decimalPad)
                        .padding()
                        .background(Color(hex: "171B26"))
                        .foregroundColor(.white)
                        .cornerRadius(4)
                }
                
                // 2. 网格数量
                sectionHeader(title: "2. 网格数量", trailingText: "")
                
                HStack {
                    TextField("2-170", text: $gridCount)
                        .padding()
                        .background(Color(hex: "171B26"))
                        .foregroundColor(.white)
                        .cornerRadius(4)
                    
                    Text("Arithmetic")
                        .foregroundColor(.white)
                        .padding(10)
                        .background(Color(hex: "171B26"))
                        .cornerRadius(4)
                        .overlay(
                            HStack {
                                Spacer()
                                Image(systemName: "chevron.down")
                                    .foregroundColor(.white)
                                    .font(.system(size: 12))
                                    .padding(.trailing, 8)
                            }
                        )
                }
                
                Text("Profit/grid(fees deducted)")
                    .font(.system(size: 14))
                    .foregroundColor(.gray)
                
                Text("--")
                    .foregroundColor(.white)
                    .font(.system(size: 16))
                
                // 3. 投资额
                sectionHeader(title: "3. 投资额", trailingText: "USDT")
                
                HStack {
                    TextField("", text: $investment)
                        .keyboardType(.decimalPad)
                        .padding()
                        .background(Color(hex: "171B26"))
                        .foregroundColor(.white)
                        .cornerRadius(4)
                    
                    Text("USDT")
                        .foregroundColor(.white)
                        .padding(.horizontal, 12)
                        .padding(.vertical, 8)
                }
                
                HStack {
                    Text("可用")
                        .font(.system(size: 14))
                        .foregroundColor(.gray)
                    Spacer()
                    Text("0.00 USDT")
                        .foregroundColor(.white)
                        .font(.system(size: 14))
                }
                
                // 高级选项（可选）
                advancedOptionsSection
                
                // 注册按钮
                Button(action: {
                    // 注册逻辑
                }) {
                    Text("注册")
                        .font(.headline)
                        .foregroundColor(Color(hex: "171B26"))
                        .frame(maxWidth: .infinity)
                        .padding()
                        .background(Color.yellow)
                        .cornerRadius(4)
                }
                .padding(.top)
                
                // 登录按钮
                Button(action: {
                    // 登录逻辑
                }) {
                    Text("登录")
                        .font(.headline)
                        .foregroundColor(.white)
                        .frame(maxWidth: .infinity)
                        .padding()
                        .background(Color(hex: "252932"))
                        .cornerRadius(4)
                }
            }
            .padding()
        }
        .background(Color(hex: "0D1119"))
    }
    
    // 高级选项部分
    private var advancedOptionsSection: some View {
        VStack(alignment: .leading, spacing: 15) {
            HStack {
                Text("高级选项（可选）")
                    .font(.headline)
                    .foregroundColor(.white)
                
                Spacer()
                
                Image(systemName: "chevron.down")
                    .foregroundColor(.gray)
                    .rotationEffect(Angle(degrees: 180))
            }
            
            // 高级选项内容
            Toggle(isOn: $isTrailingUp) {
                Text("追踪上升")
                    .foregroundColor(.white)
                    .font(.system(size: 16))
            }
            .toggleStyle(CustomToggleStyle())
            
            Toggle(isOn: $isGridTrigger) {
                Text("网格触发器")
                    .foregroundColor(.white)
                    .font(.system(size: 16))
            }
            .toggleStyle(CustomToggleStyle())
            
            Toggle(isOn: $isTPSL) {
                Text("TP/SL")
                    .foregroundColor(.white)
                    .font(.system(size: 16))
            }
            .toggleStyle(CustomToggleStyle())
            
            Toggle(isOn: $isSellAllOnStop) {
                Text("停止时售出所有BTC")
                    .foregroundColor(.white)
                    .font(.system(size: 16))
            }
            .toggleStyle(CustomToggleStyle())
        }
        .padding()
        .background(Color(hex: "171B26").opacity(0.5))
        .cornerRadius(8)
    }
    
    // 部分标题
    private func sectionHeader(title: String, trailingText: String) -> some View {
        HStack {
            Text(title)
                .font(.headline)
                .foregroundColor(.white)
            
            Spacer()
            
            if !trailingText.isEmpty {
                Text(trailingText)
                    .font(.system(size: 14))
                    .foregroundColor(.yellow)
            }
        }
    }
    
    // 策略按钮
    private func strategyButton(title: String, isSelected: Bool) -> some View {
        Button(action: {}) {
            Text(title)
                .font(.system(size: 14))
                .foregroundColor(isSelected ? .white : .gray)
                .frame(maxWidth: .infinity)
                .padding(.vertical, 10)
        }
        .background(isSelected ? Color.clear : Color.clear)
        .overlay(
            Rectangle()
                .frame(height: 3)
                .foregroundColor(isSelected ? .yellow : .clear)
                .offset(y: 12),
            alignment: .bottom
        )
    }
}

// 自定义Toggle样式
struct CustomToggleStyle: ToggleStyle {
    func makeBody(configuration: Configuration) -> some View {
        HStack {
            configuration.label
            Spacer()
            Rectangle()
                .foregroundColor(configuration.isOn ? .yellow : Color(hex: "252932"))
                .frame(width: 50, height: 28)
                .cornerRadius(14)
                .overlay(
                    Circle()
                        .foregroundColor(.white)
                        .padding(3)
                        .offset(x: configuration.isOn ? 11 : -11, y: 0)
                )
                .onTapGesture {
                    withAnimation(.spring()) {
                        configuration.isOn.toggle()
                    }
                }
        }
    }
}

struct SpotGridView_Previews: PreviewProvider {
    static var previews: some View {
        SpotGridView()
    }
} 