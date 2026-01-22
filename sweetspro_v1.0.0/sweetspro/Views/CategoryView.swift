import SwiftUI

struct CategoryView: View {
    let categories = MockData.categories
    @State private var searchText = ""
    
    
    var filteredCategories: [Category] {
        if searchText.isEmpty {
            return categories
        }
        return categories.filter { $0.name.contains(searchText) || $0.englishName.lowercased().contains(searchText.lowercased()) }
    }
    
    var searchResults: [Product] {
        if searchText.isEmpty {
            return []
        }
        return MockData.allProducts.filter { 
            $0.name.contains(searchText) || 
            $0.category.contains(searchText) ||
            $0.description.contains(searchText)
        }
    }
    
    var body: some View {
        NavigationView {
            List {
                if !searchText.isEmpty && !searchResults.isEmpty {
                    Section(header: Text("検索結果").font(.headline)) {
                        ForEach(searchResults) { product in
                            NavigationLink(destination: ProductDetailView(product: product)) {
                                HStack {
                                    AsyncImage(url: URL(string: product.imageUrl)) { phase in
                                        switch phase {
                                        case .success(let image):
                                            image.resizable().aspectRatio(contentMode: .fill)
                                        default:
                                            Color.gray.opacity(0.2)
                                        }
                                    }
                                    .frame(width: 50, height: 50)
                                    .cornerRadius(4)
                                    
                                    VStack(alignment: .leading) {
                                        Text(product.name)
                                            .font(.body)
                                        Text("¥\(product.price)")
                                            .font(.caption)
                                            .foregroundColor(.red)
                                    }
                                }
                            }
                        }
                    }
                }
                
                Section(header: Text("カテゴリー").font(.headline)) {
                    ForEach(filteredCategories) { category in
                        NavigationLink(destination: CategoryResultView(category: category)) {
                            HStack {
                                Circle()
                                    .fill(Color.sweetsBrown.opacity(0.8))
                                    .frame(width: 8, height: 8)
                                Text(category.name)
                                    .font(.body)
                                Spacer()
                                Text(category.englishName)
                                    .font(.caption)
                                    .foregroundColor(.gray)
                            }
                            .padding(.vertical, 8)
                        }
                    }
                }
            }
            .navigationTitle("商品検索")
            .searchable(text: $searchText, prompt: "キーワードで検索")
        }
    }
}

struct CategoryResultView: View {
    let category: Category
    @State private var sortOption: SortOption = .standard
    
    enum SortOption: String, CaseIterable, Identifiable {
        case standard = "標準"
        case priceLowToHigh = "価格が安い順"
        case priceHighToLow = "価格が高い順"
        
        var id: String { self.rawValue }
    }
    
    var filteredProducts: [Product] {
        let raw = MockData.allProducts.filter { $0.category == category.name }
        switch sortOption {
        case .standard:
            return raw
        case .priceLowToHigh:
            return raw.sorted { $0.price < $1.price }
        case .priceHighToLow:
            return raw.sorted { $0.price > $1.price }
        }
    }
    
    var body: some View {
        ScrollView {
            VStack {
                // Sorting Controls
                HStack {
                    Spacer()
                    Menu {
                        Picker("並び替え", selection: $sortOption) {
                            ForEach(SortOption.allCases) { option in
                                Text(option.rawValue).tag(option)
                            }
                        }
                    } label: {
                        HStack {
                            Image(systemName: "arrow.up.arrow.down")
                            Text(sortOption.rawValue)
                        }
                        .padding(8)
                        .background(Color.white)
                        .cornerRadius(8)
                        .shadow(radius: 1)
                    }
                }
                .padding(.horizontal)
                .padding(.top, 10)
                
                if filteredProducts.isEmpty {
                    VStack(spacing: 20) {
                        Image(systemName: "shippingbox")
                            .font(.system(size: 50))
                            .foregroundColor(.gray)
                        Text("該当する商品がありません")
                            .foregroundColor(.gray)
                    }
                    .padding(.top, 50)
                } else {
                    LazyVGrid(columns: [GridItem(.flexible()), GridItem(.flexible())], spacing: 15) {
                        ForEach(filteredProducts) { product in
                            NavigationLink(destination: ProductDetailView(product: product)) {
                                ProductCell(product: product)
                            }
                        }
                    }
                    .padding()
                }
            }
        }
        .navigationTitle(category.name)
        .background(Color(UIColor.systemGroupedBackground))
    }
}
