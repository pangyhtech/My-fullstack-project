import SwiftUI

@main
struct SweetsProApp: App {
    @StateObject private var appState = AppState()
    @StateObject private var userManager = UserManager()
    @StateObject private var orderManager = OrderManager()
    @StateObject private var couponManager = CouponManager()
    
    var body: some Scene {
        WindowGroup {
            ContentView()
                .environmentObject(appState)
                .environmentObject(userManager)
                .environmentObject(orderManager)
                .environmentObject(couponManager)
        }
    }
}
