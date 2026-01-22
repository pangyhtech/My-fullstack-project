import Foundation
import Combine

// Review Model
struct Review: Identifiable, Codable {
    let id: String
    let productId: String
    let userId: String
    let userName: String
    let rating: Int // 1-5
    let comment: String
    let date: String
    
    init(id: String = UUID().uuidString, productId: String, userId: String, userName: String, rating: Int, comment: String, date: String = ISO8601DateFormatter().string(from: Date())) {
        self.id = id
        self.productId = productId
        self.userId = userId
        self.userName = userName
        self.rating = rating
        self.comment = comment
        self.date = date
    }
}

// Membership Tier enum (must be before SweetsUser)
enum MembershipTier: String, Codable {
    case regular = "レギュラー"
    case silver = "シルバー"
    case gold = "ゴールド"
    case platinum = "プラチナ"
    
    var requiredPoints: Int {
        switch self {
        case .regular: return 0
        case .silver: return 1000
        case .gold: return 5000
        case .platinum: return 10000
        }
    }
    
    var discountRate: Double {
        switch self {
        case .regular: return 0.0
        case .silver: return 0.05
        case .gold: return 0.10
        case .platinum: return 0.15
        }
    }
    
    var color: String {
        switch self {
        case .regular: return "gray"
        case .silver: return "silver"
        case .gold: return "gold"
        case .platinum: return "purple"
        }
    }
}

// SweetsUser Model (renamed to avoid Foundation.User conflict)
struct SweetsUser: Identifiable, Codable {
    let id: String
    var name: String
    var email: String
    var phoneNumber: String
    var postalCode: String
    var address: String
    var favoriteProductIds: [String]
    var membershipTier: MembershipTier
    var points: Int
    var totalSpent: Int
    var couponIds: [String]
    var createdAt: String
    
    init(id: String = UUID().uuidString, 
         name: String, 
         email: String, 
         phoneNumber: String = "",
         postalCode: String = "",
         address: String = "",
         favoriteProductIds: [String] = [],
         membershipTier: MembershipTier = .regular,
         points: Int = 0,
         totalSpent: Int = 0,
         couponIds: [String] = [],
         createdAt: String = ISO8601DateFormatter().string(from: Date())) {
        self.id = id
        self.name = name
        self.email = email
        self.phoneNumber = phoneNumber
        self.postalCode = postalCode
        self.address = address
        self.favoriteProductIds = favoriteProductIds
        self.membershipTier = membershipTier
        self.points = points
        self.totalSpent = totalSpent
        self.couponIds = couponIds
        self.createdAt = createdAt
    }
}

// Mock current user for demo
class UserManager: ObservableObject {
    @Published var currentUser: SweetsUser?
    @Published var favorites: Set<String> = []
    
    init() {
        // Mock user
        self.currentUser = SweetsUser(
            id: "user_001",
            name: "田中太郎",
            email: "tanaka@example.com",
            phoneNumber: "090-1234-5678",
            postalCode: "150-0001",
            address: "東京都渋谷区神宮前1-2-3",
            favoriteProductIds: [],
            membershipTier: .silver,
            points: 1500,
            totalSpent: 15000
        )
        // Initialize favorites from user data
        self.favorites = Set(currentUser?.favoriteProductIds ?? [])
    }
    
    func toggleFavorite(productId: String) {
        if favorites.contains(productId) {
            favorites.remove(productId)
        } else {
            favorites.insert(productId)
        }
        currentUser?.favoriteProductIds = Array(favorites)
        // In production, sync to backend here
    }
    
    func isFavorite(productId: String) -> Bool {
        return favorites.contains(productId)
    }
    
    func updateUserInfo(name: String, email: String, phoneNumber: String, postalCode: String, address: String) {
        currentUser?.name = name
        currentUser?.email = email
        currentUser?.phoneNumber = phoneNumber
        currentUser?.postalCode = postalCode
        currentUser?.address = address
        // In production, sync to backend here
    }
    
    func addPoints(_ points: Int) {
        currentUser?.points += points
        checkMembershipUpgrade()
        // Sync to backend
    }
    
    func addPurchase(amount: Int) {
        currentUser?.totalSpent += amount
        // Add 1% of purchase as points
        addPoints(amount / 100)
        // Sync to backend
    }
    
    func checkMembershipUpgrade() {
        guard let user = currentUser else { return }
        
        if user.points >= MembershipTier.platinum.requiredPoints {
            currentUser?.membershipTier = MembershipTier.platinum
        } else if user.points >= MembershipTier.gold.requiredPoints {
            currentUser?.membershipTier = MembershipTier.gold
        } else if user.points >= MembershipTier.silver.requiredPoints {
            currentUser?.membershipTier = MembershipTier.silver
        }
    }
    
    func deleteAccount() {
        // In production, call backend API to delete account
        currentUser = nil
        favorites.removeAll()
        // Navigate to login screen
    }
}
