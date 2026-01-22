import SwiftUI

struct FavoritesView: View {
    @EnvironmentObject var userManager: UserManager
    
    var favoriteProducts: [Product] {
        MockData.allProducts.filter { product in
            userManager.isFavorite(productId: product.name)
        }
    }
    
    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 20) {
                Text("お気に入り商品")
                    .font(.title2)
                    .fontWeight(.bold)
                    .foregroundColor(.sweetsBrown)
                    .padding(.horizontal)
                    .padding(.top)
                
                if favoriteProducts.isEmpty {
                    VStack(spacing: 20) {
                        Image(systemName: "heart.slash")
                            .font(.system(size: 60))
                            .foregroundColor(.gray)
                        Text("お気に入りの商品がありません")
                            .foregroundColor(.gray)
                        Text("商品詳細ページで♡をタップして追加できます")
                            .font(.caption)
                            .foregroundColor(.gray)
                    }
                    .frame(maxWidth: .infinity)
                    .padding(.top, 100)
                } else {
                    LazyVGrid(columns: [GridItem(.flexible()), GridItem(.flexible())], spacing: 15) {
                        ForEach(favoriteProducts) { product in
                            NavigationLink(destination: ProductDetailView(product: product)) {
                                ProductCell(product: product)
                            }
                        }
                    }
                    .padding(.horizontal)
                }
            }
        }
        .navigationBarTitleDisplayMode(.inline)
        .background(Color(UIColor.systemGroupedBackground))
    }
}
