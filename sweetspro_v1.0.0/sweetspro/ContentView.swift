import SwiftUI

struct ContentView: View {
    @EnvironmentObject var appState: AppState
    
    var body: some View {
        TabView {
            HomeView()
                .environmentObject(appState)
                .tabItem {
                    Image(systemName: "house")
                    Text("ホーム")
                }
            
            CategoryView()
                .environmentObject(appState)
                .tabItem {
                    Image(systemName: "magnifyingglass")
                    Text("検索")
                }
            
            CartView()
                .environmentObject(appState)
                .tabItem {
                    Image(systemName: "cart")
                    Text("カート")
                }
                .badge(appState.cartCount > 0 ? "\(appState.cartCount)" : nil)
            
            MyPageView()
                .environmentObject(appState)
                .tabItem {
                    Image(systemName: "person")
                    Text("マイページ")
                }
        }
        .accentColor(.sweetsBrown)
    }
}
