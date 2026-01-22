import SwiftUI

struct CartView: View {
    @EnvironmentObject var appState: AppState
    @State private var showingCheckoutAlert = false
    
    var body: some View {
        NavigationView {
            VStack {
                if appState.cartItems.isEmpty {
                    VStack(spacing: 20) {
                        Image(systemName: "cart.badge.minus")
                            .font(.system(size: 60))
                            .foregroundColor(.gray)
                        Text("カートに商品がありません")
                            .font(.headline)
                            .foregroundColor(.gray)
                    }
                } else {
                    ScrollView {
                        ForEach(appState.cartItems) { item in
                            CartItemRow(item: item)
                                .padding(.horizontal)
                                .padding(.top)
                        }
                    }
                    
                    // Footer / Checkout Area
                    VStack(spacing: 15) {
                        Divider()
                        
                        HStack {
                            Text("小計")
                                .foregroundColor(.gray)
                            Spacer()
                            Text("¥\(appState.cartTotal)")
                                .font(.title2)
                                .fontWeight(.bold)
                        }
                        .padding(.horizontal)
                        
                        
                        NavigationLink(destination: CheckoutView()) {
                            Text("レジに進む")
                                .font(.headline)
                                .foregroundColor(.white)
                                .frame(maxWidth: .infinity)
                                .padding()
                                .background(Color.red)
                                .cornerRadius(8)
                        }
                        .padding(.horizontal)
                        .padding(.bottom)
                    }
                    .background(Color.white)
                    .shadow(radius: 2)
                }
            }
            .navigationTitle("カート")
            .background(Color(UIColor.systemGroupedBackground))
        }
    }
}

struct CartItemRow: View {
    let item: CartItem
    @EnvironmentObject var appState: AppState
    
    var body: some View {
        HStack(spacing: 15) {
            AsyncImage(url: URL(string: item.product.imageUrl)) { phase in
                if let image = phase.image {
                    image.resizable().aspectRatio(contentMode: .fill)
                } else {
                    Color.gray.opacity(0.1)
                }
            }
            .frame(width: 80, height: 80)
            .cornerRadius(4)
            .clipped()
            
            VStack(alignment: .leading, spacing: 5) {
                Text(item.product.name)
                    .font(.subheadline)
                    .lineLimit(2)
                    .foregroundColor(.sweetsBrown)
                
                Text("¥\(item.product.price)")
                    .font(.headline)
                
                HStack {
                    Text("数量: \(item.quantity)")
                        .font(.caption)
                        .foregroundColor(.gray)
                    Spacer()
                    Button(action: { appState.removeFromCart(id: item.id) }) {
                        Text("削除")
                            .font(.caption)
                            .foregroundColor(.red)
                    }
                }
            }
        }
        .padding()
        .background(Color.white)
        .cornerRadius(8)
        .shadow(color: Color.black.opacity(0.05), radius: 2)
    }
}
