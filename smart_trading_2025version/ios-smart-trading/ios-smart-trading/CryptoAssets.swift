import SwiftUI

struct CoinIcon: View {
    var symbol: String
    var size: CGFloat = 24
    
    var body: some View {
        ZStack {
            Circle()
                .fill(coinColor(for: symbol))
                .frame(width: size, height: size)
            
            Text(String(symbol.prefix(1)))
                .font(.system(size: size * 0.5, weight: .bold))
                .foregroundColor(.white)
        }
    }
    
    private func coinColor(for symbol: String) -> Color {
        switch symbol.lowercased() {
        case "btc":
            return Color(hex: "F7931A")
        case "eth":
            return Color(hex: "627EEA")
        case "bnb":
            return Color(hex: "F3BA2F")
        case "sol":
            return Color(hex: "00FFA3")
        case "xrp":
            return Color(hex: "23292F")
        case "doge":
            return Color(hex: "C2A633")
        case "dot":
            return Color(hex: "E6007A")
        case "avax":
            return Color(hex: "E84142")
        case "ltc":
            return Color(hex: "345D9D")
        case "link":
            return Color(hex: "2A5ADA")
        default:
            return Color(hex: "888888")
        }
    }
}

// 扩展帮助显示币种和交易对
extension String {
    // 获取交易对的基础货币
    var baseCurrency: String {
        if self.hasSuffix("USDT") {
            return String(self.dropLast(4))
        } else if self.hasSuffix("BTC") {
            return String(self.dropLast(3))
        } else if self.hasSuffix("ETH") {
            return String(self.dropLast(3))
        } else {
            return self
        }
    }
    
    // 获取交易对的报价货币
    var quoteCurrency: String {
        if self.hasSuffix("USDT") {
            return "USDT"
        } else if self.hasSuffix("BTC") {
            return "BTC"
        } else if self.hasSuffix("ETH") {
            return "ETH"
        } else {
            return ""
        }
    }
}

struct CoinIcon_Previews: PreviewProvider {
    static var previews: some View {
        HStack(spacing: 16) {
            CoinIcon(symbol: "BTC")
            CoinIcon(symbol: "ETH")
            CoinIcon(symbol: "SOL")
            CoinIcon(symbol: "XRP")
        }
        .padding()
        .background(Color(hex: "0D1119"))
        .previewLayout(.sizeThatFits)
    }
} 