import Foundation
import Combine

// Order Model
struct Order: Identifiable, Codable {
    let id: String
    let userId: String
    let items: [OrderItem]
    let totalAmount: Int
    let deliveryFee: Int
    let deliveryDate: String
    let deliveryTime: String
    let paymentMethod: String
    let status: OrderStatus
    let createdAt: String
    
    var displayTotal: Int {
        return totalAmount + deliveryFee
    }
    
    init(id: String = UUID().uuidString,
         userId: String,
         items: [OrderItem],
         totalAmount: Int,
         deliveryFee: Int,
         deliveryDate: String,
         deliveryTime: String,
         paymentMethod: String,
         status: OrderStatus = .pending,
         createdAt: String = ISO8601DateFormatter().string(from: Date())) {
        self.id = id
        self.userId = userId
        self.items = items
        self.totalAmount = totalAmount
        self.deliveryFee = deliveryFee
        self.deliveryDate = deliveryDate
        self.deliveryTime = deliveryTime
        self.paymentMethod = paymentMethod
        self.status = status
        self.createdAt = createdAt
    }
}

struct OrderItem: Codable {
    let productName: String
    let productPrice: Int
    let quantity: Int
    
    var subtotal: Int {
        return productPrice * quantity
    }
}

enum OrderStatus: String, Codable {
    case pending = "注文受付"
    case confirmed = "注文確定"
    case preparing = "準備中"
    case shipped = "発送済み"
    case delivered = "配達完了"
    case cancelled = "キャンセル"
}

// Coupon Model
struct Coupon: Identifiable, Codable {
    let id: String
    let code: String
    let title: String
    let discountType: DiscountType
    let discountValue: Int
    let minPurchase: Int
    let expiryDate: String
    let isUsed: Bool
    
    init(id: String = UUID().uuidString,
         code: String,
         title: String,
         discountType: DiscountType,
         discountValue: Int,
         minPurchase: Int = 0,
         expiryDate: String,
         isUsed: Bool = false) {
        self.id = id
        self.code = code
        self.title = title
        self.discountType = discountType
        self.discountValue = discountValue
        self.minPurchase = minPurchase
        self.expiryDate = expiryDate
        self.isUsed = isUsed
    }
}

enum DiscountType: String, Codable {
    case percentage = "割引率"
    case fixed = "固定金額"
}

// Order Manager
class OrderManager: ObservableObject {
    @Published var orders: [Order] = []
    
    func createOrder(userId: String, items: [CartItem], totalAmount: Int, deliveryFee: Int, deliveryDate: Date, deliveryTime: String, paymentMethod: String) -> Order {
        let orderItems = items.map { OrderItem(productName: $0.product.name, productPrice: $0.product.price, quantity: $0.quantity) }
        
        let dateFormatter = DateFormatter()
        dateFormatter.dateFormat = "yyyy年MM月dd日"
        
        let order = Order(
            userId: userId,
            items: orderItems,
            totalAmount: totalAmount,
            deliveryFee: deliveryFee,
            deliveryDate: dateFormatter.string(from: deliveryDate),
            deliveryTime: deliveryTime,
            paymentMethod: paymentMethod
        )
        
        orders.insert(order, at: 0)
        return order
    }
    
    func getUserOrders(userId: String) -> [Order] {
        return orders.filter { $0.userId == userId }
    }
}

// Coupon Manager
class CouponManager: ObservableObject {
    @Published var coupons: [Coupon] = []
    
    init() {
        loadMockCoupons()
    }
    
    func loadMockCoupons() {
        let dateFormatter = ISO8601DateFormatter()
        let futureDate = Date().addingTimeInterval(86400 * 30) // 30 days from now
        
        coupons = [
            Coupon(
                code: "WELCOME10",
                title: "新規会員限定10%OFF",
                discountType: .percentage,
                discountValue: 10,
                minPurchase: 3000,
                expiryDate: dateFormatter.string(from: futureDate)
            ),
            Coupon(
                code: "SAVE500",
                title: "500円OFFクーポン",
                discountType: .fixed,
                discountValue: 500,
                minPurchase: 5000,
                expiryDate: dateFormatter.string(from: futureDate)
            ),
            Coupon(
                code: "BIRTHDAY15",
                title: "お誕生日特典15%OFF",
                discountType: .percentage,
                discountValue: 15,
                minPurchase: 0,
                expiryDate: dateFormatter.string(from: futureDate)
            )
        ]
    }
    
    func getAvailableCoupons() -> [Coupon] {
        return coupons.filter { !$0.isUsed }
    }
}
