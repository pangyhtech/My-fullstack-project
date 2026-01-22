import SwiftUI

struct OrderHistoryView: View {
    @EnvironmentObject var orderManager: OrderManager
    @EnvironmentObject var userManager: UserManager
    
    var userOrders: [Order] {
        guard let userId = userManager.currentUser?.id else { return [] }
        return orderManager.getUserOrders(userId: userId)
    }
    
    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 20) {
                Text("購入履歴")
                    .font(.title2)
                    .fontWeight(.bold)
                    .foregroundColor(.sweetsBrown)
                    .padding(.horizontal)
                    .padding(.top)
                
                if userOrders.isEmpty {
                    VStack(spacing: 20) {
                        Image(systemName: "bag")
                            .font(.system(size: 60))
                            .foregroundColor(.gray)
                        Text("購入履歴がありません")
                            .foregroundColor(.gray)
                    }
                    .frame(maxWidth: .infinity)
                    .padding(.top, 100)
                } else {
                    ForEach(userOrders) { order in
                        NavigationLink(destination: OrderDetailView(order: order)) {
                            OrderRowView(order: order)
                        }
                        .padding(.horizontal)
                    }
                }
            }
        }
        .navigationBarTitleDisplayMode(.inline)
        .background(Color(UIColor.systemGroupedBackground))
    }
}

struct OrderRowView: View {
    let order: Order
    
    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            HStack {
                Text("注文番号: \(order.id.prefix(8))")
                    .font(.caption)
                    .foregroundColor(.gray)
                Spacer()
                Text(order.status.rawValue)
                    .font(.caption)
                    .padding(.horizontal, 8)
                    .padding(.vertical, 4)
                    .background(statusColor(for: order.status))
                    .foregroundColor(.white)
                    .cornerRadius(4)
            }
            
            Text(formatDate(order.createdAt))
                .font(.caption)
                .foregroundColor(.gray)
            
            ForEach(order.items.indices, id: \.self) { index in
                HStack {
                    Text(order.items[index].productName)
                        .font(.subheadline)
                    Spacer()
                    Text("×\(order.items[index].quantity)")
                        .font(.caption)
                        .foregroundColor(.gray)
                }
            }
            
            Divider()
            
            HStack {
                Text("合計")
                    .font(.headline)
                Spacer()
                Text("¥\(order.displayTotal)")
                    .font(.headline)
                    .foregroundColor(.red)
            }
        }
        .padding()
        .background(Color.white)
        .cornerRadius(8)
        .shadow(color: Color.black.opacity(0.05), radius: 2)
    }
    
    func statusColor(for status: OrderStatus) -> Color {
        switch status {
        case .pending: return .orange
        case .confirmed: return .blue
        case .preparing: return .purple
        case .shipped: return .green
        case .delivered: return .gray
        case .cancelled: return .red
        }
    }
    
    func formatDate(_ isoString: String) -> String {
        let formatter = ISO8601DateFormatter()
        guard let date = formatter.date(from: isoString) else { return isoString }
        let displayFormatter = DateFormatter()
        displayFormatter.dateStyle = .medium
        displayFormatter.timeStyle = .short
        displayFormatter.locale = Locale(identifier: "ja_JP")
        return displayFormatter.string(from: date)
    }
}

struct OrderDetailView: View {
    let order: Order
    
    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 20) {
                // Order Status
                VStack(alignment: .leading, spacing: 8) {
                    Text("注文状況")
                        .font(.headline)
                    Text(order.status.rawValue)
                        .font(.title3)
                        .foregroundColor(.sweetsBrown)
                }
                
                Divider()
                
                // Order Items
                VStack(alignment: .leading, spacing: 12) {
                    Text("注文内容")
                        .font(.headline)
                    
                    ForEach(order.items.indices, id: \.self) { index in
                        HStack {
                            VStack(alignment: .leading) {
                                Text(order.items[index].productName)
                                    .font(.body)
                                Text("¥\(order.items[index].productPrice) × \(order.items[index].quantity)")
                                    .font(.caption)
                                    .foregroundColor(.gray)
                            }
                            Spacer()
                            Text("¥\(order.items[index].subtotal)")
                                .font(.body)
                        }
                        .padding(.vertical, 4)
                    }
                }
                
                Divider()
                
                // Delivery Info
                VStack(alignment: .leading, spacing: 8) {
                    Text("配送情報")
                        .font(.headline)
                    Text("配送日: \(order.deliveryDate)")
                        .font(.body)
                    Text("時間帯: \(order.deliveryTime)")
                        .font(.body)
                }
                
                Divider()
                
                // Payment
                VStack(alignment: .leading, spacing: 8) {
                    Text("お支払い")
                        .font(.headline)
                    HStack {
                        Text("商品合計")
                        Spacer()
                        Text("¥\(order.totalAmount)")
                    }
                    HStack {
                        Text("配送料")
                        Spacer()
                        Text(order.deliveryFee == 0 ? "無料" : "¥\(order.deliveryFee)")
                    }
                    Divider()
                    HStack {
                        Text("合計金額")
                            .fontWeight(.bold)
                        Spacer()
                        Text("¥\(order.displayTotal)")
                            .fontWeight(.bold)
                            .foregroundColor(.red)
                    }
                    Text("支払い方法: \(order.paymentMethod)")
                        .font(.caption)
                        .foregroundColor(.gray)
                        .padding(.top, 4)
                }
            }
            .padding()
        }
        .navigationTitle("注文詳細")
        .navigationBarTitleDisplayMode(.inline)
        .background(Color(UIColor.systemGroupedBackground))
    }
}
