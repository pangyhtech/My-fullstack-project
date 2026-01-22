import SwiftUI

struct ProductDetailView: View {
    let product: Product
    @EnvironmentObject var appState: AppState
    @EnvironmentObject var userManager: UserManager
    @State private var quantity: Int = 1
    @State private var selectedImageIndex: Int = 0
    @State private var showReviewSheet: Bool = false
    @State private var newReviewRating: Int = 5
    @State private var newReviewComment: String = ""
    @Environment(\.presentationMode) var presentationMode
    
    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 0) {
                // Image Gallery
                TabView(selection: $selectedImageIndex) {
                    ForEach(0..<product.images.count, id: \.self) { index in
                        AsyncImage(url: URL(string: product.images[index])) { phase in
                            switch phase {
                            case .empty: Color.gray.opacity(0.1)
                            case .success(let image): 
                                image.resizable().aspectRatio(contentMode: .fit)
                            case .failure: Color.gray.opacity(0.1)
                            @unknown default: EmptyView()
                            }
                        }
                        .tag(index)
                    }
                }
                .tabViewStyle(PageTabViewStyle())
                .frame(height: 300)
                .background(Color.white)
                
                // Content
                VStack(alignment: .leading, spacing: 20) {
                    // Title and Price
                    VStack(alignment: .leading, spacing: 8) {
                        Text(product.name)
                            .font(.title2)
                            .fontWeight(.bold)
                            .foregroundColor(.sweetsBrown)
                        
                        HStack(alignment: .lastTextBaseline) {
                            Text("¥\(product.price)")
                                .font(.title)
                                .fontWeight(.bold)
                                .foregroundColor(.red)
                            Text("(税込)")
                                .font(.caption)
                                .foregroundColor(.gray)
                        }
                    }
                    
                    HStack {
                        Divider()
                        Button(action: {
                            userManager.toggleFavorite(productId:product.name)
                        }) {
                            HStack {
                                Image(systemName: userManager.isFavorite(productId: product.name) ? "heart.fill" : "heart")
                                    .foregroundColor(.red)
                                Text("お気に入り")
                                    .font(.caption)
                                    .foregroundColor(.black)
                            }
                        }
                    }
                    .frame(height: 40)
                    
                    Divider()
                    
                    // Quantity Selector
                    HStack {
                        Text("数量")
                            .font(.headline)
                        Spacer()
                        HStack(spacing: 20) {
                            Button(action: { if quantity > 1 { quantity -= 1 } }) {
                                Image(systemName: "minus.circle.fill")
                                    .font(.title2)
                                    .foregroundColor(.gray)
                            }
                            Text("\(quantity)")
                                .font(.title3)
                                .frame(width: 40)
                            Button(action: { quantity += 1 }) {
                                Image(systemName: "plus.circle.fill")
                                    .font(.title2)
                                    .foregroundColor(.sweetsBrown)
                            }
                        }
                    }
                    .padding(.vertical, 5)
                    
                    // Add to Cart Button
                    Button(action: {
                        appState.addToCart(product: product, quantity: quantity)
                        presentationMode.wrappedValue.dismiss()
                    }) {
                        Text("カートに入れる")
                            .font(.headline)
                            .fontWeight(.bold)
                            .foregroundColor(.white)
                            .frame(maxWidth: .infinity)
                            .padding()
                            .background(Color.sweetsBrown)
                            .cornerRadius(8)
                    }
                    
                    Divider()
                    
                    // Description
                    if !product.description.isEmpty {
                        VStack(alignment: .leading, spacing: 10) {
                            Text("商品説明")
                                .font(.headline)
                            Text(product.description)
                                .font(.body)
                                .foregroundColor(.secondary)
                                .lineSpacing(4)
                        }
                    }
                    
                    // Technical Details (Accordion style)
                    if let details = product.details {
                        DetailRow(title: "原材料", content: details.ingredients)
                        DetailRow(title: "栄養成分", content: details.nutrition)
                        DetailRow(title: "賞味期限", content: details.expiration)
                        DetailRow(title: "保存方法", content: details.storage)
                    }
                    
                    Divider().padding(.top)
                    
                    // Reviews Section
                    VStack(alignment: .leading, spacing: 15) {
                        HStack {
                            Text("カスタマーレビュー")
                                .font(.headline)
                            Spacer()
                            Button(action: { showReviewSheet = true }) {
                                Text("レビューを書く")
                                    .font(.caption)
                                    .foregroundColor(.sweetsBrown)
                            }
                        }
                        
                        // Mock reviews
                        ReviewItemView(review: Review(
                            productId: product.name,
                            userId: "user_002",
                            userName: "佐藤花子",
                            rating: 5,
                            comment: "とても美味しかったです！甘さ控えめで大人の味。また購入したいです。"
                        ))
                        
                        ReviewItemView(review: Review(
                            productId: product.name,
                            userId: "user_003",
                            userName: "山田次郎",
                            rating: 4,
                            comment: "見た目も綺麗で、プレゼントに最適でした。味もとても良かったです。"
                        ))
                        
                        ReviewItemView(review: Review(
                            productId: product.name,
                            userId: "user_004",
                            userName: "鈴木美咲",
                            rating: 5,
                            comment: "このクリームの滑らかさは最高！リピート確定です。"
                        ))
                    }
                }
                .padding()
            }
        }
        .background(Color(UIColor.systemGroupedBackground))
        .navigationBarTitleDisplayMode(.inline)
    }
}

struct DetailRow: View {
    let title: String
    let content: String
    
    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            Text(title)
                .font(.subheadline)
                .fontWeight(.bold)
                .foregroundColor(.sweetsBrown)
            
            Text(content)
                .font(.caption)
                .foregroundColor(.gray)
                .padding(10)
                .frame(maxWidth: .infinity, alignment: .leading)
                .background(Color.white)
                .cornerRadius(4)
        }
    }
}
