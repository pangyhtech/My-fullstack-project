import Foundation
import SwiftUI
import Combine

// 交易对模型
struct TradingPair: Identifiable, Hashable {
    var id = UUID()
    var symbol: String
    var lastPrice: Double
    var priceChangePercent: Double
    
    var formattedPrice: String {
        let formatter = NumberFormatter()
        formatter.numberStyle = .decimal
        formatter.maximumFractionDigits = 2
        return formatter.string(from: NSNumber(value: lastPrice)) ?? "\(lastPrice)"
    }
    
    var formattedPriceChange: String {
        return priceChangePercent >= 0 ? "+\(String(format: "%.2f", priceChangePercent))%" : "\(String(format: "%.2f", priceChangePercent))%"
    }
    
    var priceChangeColor: Color {
        return priceChangePercent >= 0 ? .green : .red
    }
}

// 用户资产
struct UserAsset: Identifiable {
    var id = UUID()
    var symbol: String
    var amount: Double
    var valueInUSDT: Double
    
    var formattedAmount: String {
        return String(format: "%.8f", amount)
    }
    
    var formattedValue: String {
        return String(format: "%.2f", valueInUSDT)
    }
}

// 交易所状态模型
class ExchangeDataStore: ObservableObject {
    @Published var tradingPairs: [TradingPair] = []
    @Published var userAssets: [UserAsset] = []
    @Published var selectedPair: TradingPair?
    
    init() {
        // 加载示例数据
        loadSampleData()
    }
    
    private func loadSampleData() {
        // 示例交易对数据
        tradingPairs = [
            TradingPair(symbol: "BTCUSDT", lastPrice: 104207.73, priceChangePercent: 0.90),
            TradingPair(symbol: "ETHUSDT", lastPrice: 3405.21, priceChangePercent: 1.25),
            TradingPair(symbol: "BNBUSDT", lastPrice: 605.39, priceChangePercent: -0.45),
            TradingPair(symbol: "SOLUSDT", lastPrice: 210.63, priceChangePercent: 2.17),
            TradingPair(symbol: "ADAUSDT", lastPrice: 0.4862, priceChangePercent: -0.12)
        ]
        
        // 用户资产示例
        userAssets = [
            UserAsset(symbol: "BTC", amount: 0.025, valueInUSDT: 2605.19),
            UserAsset(symbol: "ETH", amount: 0.75, valueInUSDT: 2553.91),
            UserAsset(symbol: "USDT", amount: 1500.0, valueInUSDT: 1500.0)
        ]
        
        // 默认选择第一个交易对
        selectedPair = tradingPairs.first
    }
    
    // 获取用户USDT余额
    var usdtBalance: Double {
        return userAssets.first(where: { $0.symbol == "USDT" })?.amount ?? 0.0
    }
    
    // 格式化USDT余额
    var formattedUsdtBalance: String {
        return String(format: "%.2f", usdtBalance)
    }
} 