import SwiftUI
import Combine

class AppState: ObservableObject {
    @Published var cartItems: [CartItem] = []
    @Published var favoriteItems: [String] = [] // Product IDs
    @Published var isLoggedIn: Bool = false
    @Published var currentUser: SweetsUser?
    
    // Cart Logic
    func addToCart(product: Product, quantity: Int) {
        if let index = cartItems.firstIndex(where: { $0.product.id == product.id }) {
            cartItems[index].quantity += quantity
        } else {
            cartItems.append(CartItem(product: product, quantity: quantity))
        }
    }
    
    func removeFromCart(id: UUID) {
        cartItems.removeAll { $0.id == id }
    }
    
    func updateQuantity(id: UUID, quantity: Int) {
        if let index = cartItems.firstIndex(where: { $0.id == id }) {
            cartItems[index].quantity = quantity
        }
    }
    
    func clearCart() {
        cartItems.removeAll()
    }
    
    var cartTotal: Int {
        cartItems.reduce(0) { $0 + ($1.product.price * $1.quantity) }
    }
    
    var cartCount: Int {
        cartItems.reduce(0) { $0 + $1.quantity }
    }
    
    // Auth Logic
    func login(email: String) {
        isLoggedIn = true
        currentUser = SweetsUser(
            name: "Sweets Lover",
            email: email,
            phoneNumber: "090-0000-0000",
            postalCode: "100-0001",
            address: "Tokyo, Japan"
        )
    }
    
    func logout() {
        isLoggedIn = false
        currentUser = nil
        cartItems = []
    }
}

struct CartItem: Identifiable {
    let id = UUID()
    let product: Product
    var quantity: Int
}
