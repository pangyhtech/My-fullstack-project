import SwiftUI

struct ProductCell: View {
    let product: Product
    
    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            ZStack(alignment: .topLeading) {
                if product.imageUrl.hasPrefix("http") {
                    // Remote image
                    AsyncImage(url: URL(string: product.imageUrl)) { phase in
                        switch phase {
                        case .empty:
                            Color.gray.opacity(0.1)
                        case .success(let image):
                            image
                                .resizable()
                                .aspectRatio(contentMode: .fill)
                        case .failure:
                            Color.gray.opacity(0.2)
                        @unknown default:
                            EmptyView()
                        }
                    }
                    .frame(height: 150)
                    .clipped()
                    .background(Color.white)
                } else {
                    // Local image
                    Image(product.imageUrl)
                        .resizable()
                        .aspectRatio(contentMode: .fill)
                        .frame(height: 150)
                        .clipped()
                        .background(Color.white)
                }
                
                if let badge = product.badge {
                    Text(badge)
                        .font(.caption2)
                        .fontWeight(.bold)
                        .padding(.horizontal, 8)
                        .padding(.vertical, 4)
                        .background(Color.sweetsGold)
                        .foregroundColor(.white)
                }
            }
            .cornerRadius(4)
            
            VStack(alignment: .leading, spacing: 4) {
                Text(product.name)
                    .font(.caption)
                    .lineLimit(2)
                    .foregroundColor(.sweetsBrown)
                    .fixedSize(horizontal: false, vertical: true)
                
                Text("¥\(product.price)")
                    .font(.subheadline)
                    .fontWeight(.bold)
                    .foregroundColor(.black)
            }
            .padding(.horizontal, 4)
            .padding(.bottom, 8)
        }
        .background(Color.white)
        .cornerRadius(4)
        .shadow(color: Color.black.opacity(0.05), radius: 2, x: 0, y: 1)
    }
}
