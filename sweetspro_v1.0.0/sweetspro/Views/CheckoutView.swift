import SwiftUI

struct CheckoutView: View {
    @EnvironmentObject var appState: AppState
    @EnvironmentObject var userManager: UserManager
    @EnvironmentObject var orderManager: OrderManager
    @Environment(\.presentationMode) var presentationMode
    
    @State private var deliveryDate = Date().addingTimeInterval(86400 * 3) // 3 days from now
    @State private var deliveryTime = "指定なし"
    @State private var paymentMethod = "クレジットカード"
    @State private var navigateToSuccess = false
    @State private var orderNumber = ""

    
    let deliveryTimes = ["指定なし", "午前中(8-12時)", "14-16時", "16-18時", "18-20時", "19-21時"]
    let paymentMethods = ["クレジットカード", "代金引換", "Amazon Pay", "PayPay"]
    
    var deliveryFee: Int {
        return appState.cartTotal >= 10000 ? 0 : 800
    }
    
    var totalAmount: Int {
        return appState.cartTotal + deliveryFee
    }
    
    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 20) {
                // Header
                Text("ご注文内容の確認")
                    .font(.title2)
                    .fontWeight(.bold)
                    .foregroundColor(.sweetsBrown)
                
                Divider()
                
                // Delivery Address
                VStack(alignment: .leading, spacing: 12) {
                    Text("お届け先")
                        .font(.headline)
                    
                    VStack(alignment: .leading, spacing: 8) {
                        Text(userManager.currentUser?.name ?? "")
                            .font(.body)
                        Text("〒\(userManager.currentUser?.postalCode ?? "")")
                            .font(.caption)
                        Text(userManager.currentUser?.address ?? "")
                            .font(.caption)
                        Text("TEL: \(userManager.currentUser?.phoneNumber ?? "")")
                            .font(.caption)
                    }
                    .padding()
                    .frame(maxWidth: .infinity, alignment: .leading)
                    .background(Color.white)
                    .cornerRadius(8)
                }
                
                Divider()
                
                // Delivery Date & Time
                VStack(alignment: .leading, spacing: 12) {
                    Text("配送希望日時")
                        .font(.headline)
                    
                    DatePicker("配送希望日", selection: $deliveryDate, in: Date()..., displayedComponents: .date)
                        .datePickerStyle(.compact)
                    
                    Picker("配送時間帯", selection: $deliveryTime) {
                        ForEach(deliveryTimes, id: \.self) { time in
                            Text(time).tag(time)
                        }
                    }
                    .pickerStyle(.menu)
                }
                
                Divider()
                
                // Payment Method
                VStack(alignment: .leading, spacing: 12) {
                    Text("お支払い方法")
                        .font(.headline)
                    
                    Picker("決済方法", selection: $paymentMethod) {
                        ForEach(paymentMethods, id: \.self) { method in
                            Text(method).tag(method)
                        }
                    }
                    .pickerStyle(.segmented)
                }
                
                Divider()
                
                // Order Summary
                VStack(alignment: .leading, spacing: 12) {
                    Text("ご注文内容")
                        .font(.headline)
                    
                    ForEach(appState.cartItems) { item in
                        HStack {
                            Text(item.product.name)
                                .font(.caption)
                            Spacer()
                            Text("¥\(item.product.price) × \(item.quantity)")
                                .font(.caption)
                        }
                    }
                    
                    Divider()
                    
                    HStack {
                        Text("小計")
                        Spacer()
                        Text("¥\(appState.cartTotal)")
                    }
                    
                    HStack {
                        Text("送料")
                        Spacer()
                        if deliveryFee == 0 {
                            Text("無料")
                                .foregroundColor(.green)
                        } else {
                            Text("¥\(deliveryFee)")
                        }
                    }
                    
                    Divider()
                    
                    HStack {
                        Text("合計金額")
                            .font(.headline)
                            .fontWeight(.bold)
                        Spacer()
                        Text("¥\(totalAmount)")
                            .font(.title3)
                            .fontWeight(.bold)
                            .foregroundColor(.red)
                    }
                }
                .padding()
                .background(Color.gray.opacity(0.1))
                .cornerRadius(8)
                
                
                // Hidden NavigationLink for programmatic navigation
                NavigationLink(
                    destination: OrderSuccessView(
                        orderNumber: orderNumber,
                        totalAmount: totalAmount,
                        deliveryDate: deliveryDate,
                        deliveryTime: deliveryTime
                    )
                    .environmentObject(appState),
                    isActive: $navigateToSuccess
                ) {
                    EmptyView()
                }
                .hidden()
                
                
                // Checkout Button
                Button(action: {
                    print("🔘 注文確定ボタンがクリックされました")
                    
                    // Generate order number first
                    let newOrderNumber = createOrderWithoutClearingCart()
                    print("📋 注文番号: \(newOrderNumber)")
                    
                    // Set the order number
                    orderNumber = newOrderNumber
                    print("✅ orderNumber設定完了: \(orderNumber)")
                    
                    // Trigger navigation
                    print("🚀 ナビゲーション開始")
                    navigateToSuccess = true
                    print("✅ navigateToSuccess = \(navigateToSuccess)")
                    
                    // DON'T clear cart here - it will be cleared when user leaves OrderSuccessView
                    // This prevents the navigation stack from collapsing
                }) {
                    Text("注文を確定する")
                        .font(.headline)
                        .fontWeight(.bold)
                        .foregroundColor(.white)
                        .frame(maxWidth: .infinity)
                        .padding()
                        .background(Color.sweetsBrown)
                        .cornerRadius(8)
                }
                .padding(.top)
            }
            .padding()
        }
        .navigationBarTitleDisplayMode(.inline)
        .background(Color(UIColor.systemGroupedBackground))
    }
    
    func createOrderAndGetId() -> String {
        guard let userId = userManager.currentUser?.id else {
            return String(format: "%06d", Int.random(in: 100000...999999))
        }
        
        // Create order
        let order = orderManager.createOrder(
            userId: userId,
            items: appState.cartItems,
            totalAmount: appState.cartTotal,
            deliveryFee: deliveryFee,
            deliveryDate: deliveryDate,
            deliveryTime: deliveryTime,
            paymentMethod: paymentMethod
        )
        
        // Add purchase to user (for points)
        userManager.addPurchase(amount: totalAmount)
        
        // Clear cart
        appState.clearCart()
        
        // Return order ID (first 6 chars)
        return String(order.id.prefix(6).uppercased())
    }
    
    func createOrderWithoutClearingCart() -> String {
        guard let userId = userManager.currentUser?.id else {
            return String(format: "%06d", Int.random(in: 100000...999999))
        }
        
        // Create order
        let order = orderManager.createOrder(
            userId: userId,
            items: appState.cartItems,
            totalAmount: appState.cartTotal,
            deliveryFee: deliveryFee,
            deliveryDate: deliveryDate,
            deliveryTime: deliveryTime,
            paymentMethod: paymentMethod
        )
        
        // Add purchase to user (for points)
        userManager.addPurchase(amount: totalAmount)
        
        // DON'T clear cart here - it will be cleared after navigation
        
        // Return order ID (first 6 chars)
        return String(order.id.prefix(6).uppercased())
    }
}
