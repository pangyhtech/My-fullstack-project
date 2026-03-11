import SwiftUI

struct SmartTradingView: View {
    @State private var selectedTab = 0
    
    var body: some View {
        VStack(spacing: 0) {
            // 顶部标题栏
            HStack {
                Text("Smart Trading")
                    .font(.title)
                    .fontWeight(.bold)
                    .foregroundColor(.white)
                Spacer()
            }
            .padding()
            .background(Color(hex: "171B26"))
            
            // 选项卡切换栏
            HStack(spacing: 0) {
                tabButton(title: "Spot Grid", index: 0)
                tabButton(title: "Rebalancing", index: 1)
                tabButton(title: "Algo Order", index: 2)
            }
            .background(Color(hex: "171B26"))
            
            // 选项卡内容
            TabView(selection: $selectedTab) {
                SpotGridView()
                    .tag(0)
                
                RebalancingView()
                    .tag(1)
                
                AlgoOrderView()
                    .tag(2)
            }
            .tabViewStyle(PageTabViewStyle(indexDisplayMode: .never))
        }
        .background(Color(hex: "0D1119"))
        .edgesIgnoringSafeArea(.bottom)
    }
    
    // 选项卡按钮
    private func tabButton(title: String, index: Int) -> some View {
        Button(action: {
            withAnimation {
                selectedTab = index
            }
        }) {
            VStack(spacing: 8) {
                Text(title)
                    .font(.system(size: 16, weight: selectedTab == index ? .semibold : .regular))
                    .foregroundColor(selectedTab == index ? .white : .gray)
                
                // 底部指示器
                Rectangle()
                    .fill(selectedTab == index ? Color.yellow : Color.clear)
                    .frame(height: 3)
            }
        }
        .frame(maxWidth: .infinity)
        .padding(.vertical, 10)
    }
}

// 辅助扩展，用于从十六进制字符串创建颜色
extension Color {
    init(hex: String) {
        let scanner = Scanner(string: hex)
        var rgbValue: UInt64 = 0
        scanner.scanHexInt64(&rgbValue)
        
        let r = Double((rgbValue & 0xFF0000) >> 16) / 255.0
        let g = Double((rgbValue & 0x00FF00) >> 8) / 255.0
        let b = Double(rgbValue & 0x0000FF) / 255.0
        
        self.init(red: r, green: g, blue: b)
    }
}

struct SmartTradingView_Previews: PreviewProvider {
    static var previews: some View {
        SmartTradingView()
    }
} 