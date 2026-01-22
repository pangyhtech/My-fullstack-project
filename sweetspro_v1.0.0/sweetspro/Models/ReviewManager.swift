import Foundation
import Combine

class ReviewManager: ObservableObject {
    @Published var reviews: [String: [Review]] = [:] // productId -> [Review]
    
    init() {
        loadMockReviews()
    }
    
    func loadMockReviews() {
        // Mock reviews for demonstration
        reviews = [
            "unknown": [ // For products without specific IDs
                Review(
                    productId: "unknown",
                    userId: "user_002",
                    userName: "佐藤花子",
                    rating: 5,
                    comment: "とても美味しかったです！甘さ控えめで大人の味。また購入したいです。"
                ),
                Review(
                    productId: "unknown",
                    userId: "user_003",
                    userName: "山田次郎",
                    rating: 4,
                    comment: "見た目も綺麗で、プレゼントに最適でした。味もとても良かったです。"
                ),
                Review(
                    productId: "unknown",
                    userId: "user_004",
                    userName: "鈴木美咲",
                    rating: 5,
                    comment: "このクリームの滑らかさは最高！リピート確定です。"
                )
            ]
        ]
    }
    
    func getReviews(for productId: String) -> [Review] {
        return reviews[productId] ?? reviews["unknown"] ?? []
    }
    
    func addReview(_ review: Review) {
        if reviews[review.productId] == nil {
            reviews[review.productId] = []
        }
        reviews[review.productId]?.insert(review, at: 0)
    }
    
    func averageRating(for productId: String) -> Double {
        let productReviews = getReviews(for: productId)
        guard !productReviews.isEmpty else { return 0 }
        let sum = productReviews.reduce(0) { $0 + $1.rating }
        return Double(sum) / Double(productReviews.count)
    }
}
