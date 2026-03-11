import SwiftUI

struct RebalancingView: View {
    @State private var allocationMethod = 0 // 0: 平均分配, 1: 按市值
    @State private var coins = [
        CoinAllocation(id: 1, symbol: "BTC", percentage: 50),
        CoinAllocation(id: 2, symbol: "ETH", percentage: 50)
    ]
    @State private var totalInvestment: String = "200.00"
    @State private var rebalanceRatio = 2 // 10%
    @State private var isTriggerPrice = false
    @State private var isStopTrigger = false
    @State private var isSellAll = true
    
    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 20) {
                // AI/Manual切换
                HStack(spacing: 0) {
                    strategyButton(title: "AI", isSelected: false)
                    strategyButton(title: "Manual", isSelected: true)
                }
                .background(Color(hex: "171B26"))
                .cornerRadius(4)
                .padding(.top, 5)
                .padding(.bottom, 10)
                
                // 1. 分配方式
                VStack(alignment: .leading, spacing: 10) {
                    Text("1.分配")
                        .font(.headline)
                        .foregroundColor(.white)
                    
                    HStack(spacing: 20) {
                        allocationButton(
                            title: "平均分配",
                            isSelected: allocationMethod == 0,
                            action: { allocationMethod = 0 }
                        )
                        
                        allocationButton(
                            title: "按市值",
                            isSelected: allocationMethod == 1,
                            action: { allocationMethod = 1 }
                        )
                    }
                    
                    Button(action: {
                        // 添加币种逻辑
                    }) {
                        Text("添加币种")
                            .font(.system(size: 14))
                            .foregroundColor(.yellow)
                            .frame(maxWidth: .infinity, alignment: .trailing)
                    }
                    .padding(.top, 5)
                }
                
                // 币种分配列表
                ForEach(coins) { coin in
                    coinAllocationRow(coin: coin)
                }
                
                Text("剩余分配: 0% / 目标 100%")
                    .font(.system(size: 14))
                    .foregroundColor(.gray)
                    .padding(.top, -10)
                
                // 2. 投资币种
                VStack(alignment: .leading, spacing: 10) {
                    Text("2.投资币种")
                        .font(.headline)
                        .foregroundColor(.white)
                    
                    HStack {
                        Text("总投资")
                            .foregroundColor(.white)
                        
                        TextField("", text: $totalInvestment)
                            .keyboardType(.decimalPad)
                            .padding()
                            .background(Color(hex: "171B26"))
                            .foregroundColor(.white)
                            .cornerRadius(4)
                        
                        Text("USDT")
                            .foregroundColor(.white)
                            .padding(.horizontal, 12)
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
                }
                
                // 自动再平衡
                VStack(alignment: .leading, spacing: 10) {
                    HStack {
                        Text("自动再平衡")
                            .font(.headline)
                            .foregroundColor(.white)
                        
                        Image(systemName: "info.circle")
                            .foregroundColor(.gray)
                            .font(.system(size: 14))
                        
                        Spacer()
                        
                        Text("按币种比例: 10%")
                            .foregroundColor(.white)
                            .padding(.vertical, 6)
                            .padding(.horizontal, 10)
                            .background(Color(hex: "252932"))
                            .cornerRadius(4)
                            .overlay(
                                HStack {
                                    Spacer()
                                    Image(systemName: "chevron.down")
                                        .foregroundColor(.white)
                                        .font(.system(size: 12))
                                        .padding(.leading, 5)
                                }
                            )
                    }
                }
                
                // 高级选项（可选）
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
                    
                    Toggle(isOn: $isTriggerPrice) {
                        Text("触发价格")
                            .foregroundColor(.white)
                            .font(.system(size: 16))
                    }
                    .toggleStyle(CustomToggleStyle())
                    
                    Toggle(isOn: $isStopTrigger) {
                        Text("停止触发")
                            .foregroundColor(.white)
                            .font(.system(size: 16))
                    }
                    .toggleStyle(CustomToggleStyle())
                    
                    Toggle(isOn: $isSellAll) {
                        Text("停止时售出所有币种")
                            .foregroundColor(.white)
                            .font(.system(size: 16))
                    }
                    .toggleStyle(CustomToggleStyle())
                }
                .padding()
                .background(Color(hex: "171B26").opacity(0.5))
                .cornerRadius(8)
                
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
    
    // 币种分配行
    private func coinAllocationRow(coin: CoinAllocation) -> some View {
        HStack(spacing: 10) {
            Text("\(coin.id)")
                .foregroundColor(.white)
                .font(.system(size: 14))
            
                         HStack {
                CoinIcon(symbol: coin.symbol, size: 20)
                
                Text(coin.symbol)
                    .foregroundColor(.white)
                    .font(.system(size: 16))
                
                Image(systemName: "chevron.down")
                    .foregroundColor(.white)
                    .font(.system(size: 12))
            }
            .padding(.vertical, 8)
            .padding(.horizontal, 12)
            .background(Color(hex: "171B26"))
            .cornerRadius(4)
            
            Text("-")
                .foregroundColor(.white)
                .font(.system(size: 20))
                .frame(width: 30)
                .onTapGesture {
                    decreasePercentage(for: coin.id)
                }
            
            Text("\(coin.percentage)%")
                .foregroundColor(.white)
                .font(.system(size: 16))
                .frame(width: 50)
            
            Text("+")
                .foregroundColor(.white)
                .font(.system(size: 20))
                .frame(width: 30)
                .onTapGesture {
                    increasePercentage(for: coin.id)
                }
            
            Button(action: {
                deleteCoin(id: coin.id)
            }) {
                Image(systemName: "trash")
                    .foregroundColor(.white)
                    .font(.system(size: 16))
            }
            .frame(width: 30)
        }
        .padding(.vertical, 8)
    }
    
    // 增加百分比
    private func increasePercentage(for id: Int) {
        if let index = coins.firstIndex(where: { $0.id == id }) {
            if coins[index].percentage < 100 {
                coins[index].percentage += 1
                rebalanceOtherCoins(excluding: id)
            }
        }
    }
    
    // 减少百分比
    private func decreasePercentage(for id: Int) {
        if let index = coins.firstIndex(where: { $0.id == id }) {
            if coins[index].percentage > 0 {
                coins[index].percentage -= 1
                rebalanceOtherCoins(excluding: id)
            }
        }
    }
    
    // 重新平衡其他币种
    private func rebalanceOtherCoins(excluding id: Int) {
        let total = coins.reduce(0) { $0 + $1.percentage }
        if total != 100 && coins.count > 1 {
            let diff = 100 - total
            let otherCoins = coins.filter { $0.id != id }
            let adjustmentPerCoin = diff / otherCoins.count
            
            for coin in otherCoins {
                if let index = coins.firstIndex(where: { $0.id == coin.id }) {
                    coins[index].percentage += adjustmentPerCoin
                }
            }
        }
    }
    
    // 删除币种
    private func deleteCoin(id: Int) {
        if coins.count > 2 {
            coins.removeAll { $0.id == id }
            let totalPercentage = coins.reduce(0) { $0 + $1.percentage }
            let delta = 100 - totalPercentage
            if delta != 0 {
                let adjustment = delta / coins.count
                for i in 0..<coins.count {
                    coins[i].percentage += adjustment
                }
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
    
    // 分配方式按钮
    private func allocationButton(title: String, isSelected: Bool, action: @escaping () -> Void) -> some View {
        Button(action: action) {
            HStack {
                Circle()
                    .stroke(isSelected ? Color.yellow : Color.gray, lineWidth: 1)
                    .frame(width: 18, height: 18)
                    .overlay(
                        Circle()
                            .fill(isSelected ? Color.yellow : Color.clear)
                            .frame(width: 12, height: 12)
                    )
                
                Text(title)
                    .font(.system(size: 16))
                    .foregroundColor(.white)
            }
        }
    }
}

// 币种分配模型
struct CoinAllocation: Identifiable {
    var id: Int
    var symbol: String
    var percentage: Int
}

struct RebalancingView_Previews: PreviewProvider {
    static var previews: some View {
        RebalancingView()
    }
} 