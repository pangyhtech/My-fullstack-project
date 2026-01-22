import SwiftUI

struct OrderSuccessView: View {
    let orderNumber: String
    let totalAmount: Int
    let deliveryDate: Date
    let deliveryTime: String
    
    @EnvironmentObject var appState: AppState
    @Environment(\.presentationMode) var presentationMode
    @State private var animationProgress: CGFloat = 0
    @State private var showCheckmark = false
    @State private var showDetails = false
    
    var body: some View {
        VStack(spacing: 30) {
            Spacer()
            
            // Success Animation
            ZStack {
                // Circular Progress
                Circle()
                    .stroke(Color.gray.opacity(0.2), lineWidth: 8)
                    .frame(width: 120, height: 120)
                
                Circle()
                    .trim(from: 0, to: animationProgress)
                    .stroke(
                        Color.green,
                        style: StrokeStyle(lineWidth: 8, lineCap: .round)
                    )
                    .frame(width: 120, height: 120)
                    .rotationEffect(.degrees(-90))
                    .animation(.easeInOut(duration: 1.5), value: animationProgress)
                
                // Checkmark
                if showCheckmark {
                    Image(systemName: "checkmark")
                        .font(.system(size: 50, weight: .bold))
                        .foregroundColor(.green)
                        .transition(.scale.combined(with: .opacity))
                }
            }
            .padding(.top, 40)
            
            // Success Message
            VStack(spacing: 12) {
                Text("ご注文ありがとうございます！")
                    .font(.title2)
                    .fontWeight(.bold)
                    .foregroundColor(.sweetsBrown)
                    .opacity(showDetails ? 1 : 0)
                
                Text("ご注文を承りました")
                    .font(.body)
                    .foregroundColor(.gray)
                    .opacity(showDetails ? 1 : 0)
            }
            
            // Order Details
            if showDetails {
                VStack(spacing: 20) {
                    // Order Number
                    VStack(spacing: 8) {
                        Text("注文番号")
                            .font(.caption)
                            .foregroundColor(.gray)
                        Text("#\(orderNumber)")
                            .font(.title3)
                            .fontWeight(.bold)
                            .foregroundColor(.sweetsBrown)
                    }
                    .padding()
                    .frame(maxWidth: .infinity)
                    .background(Color.sweetsLightBg)
                    .cornerRadius(12)
                    
                    // Order Info
                    VStack(spacing: 16) {
                        HStack {
                            Image(systemName: "creditcard.fill")
                                .foregroundColor(.sweetsBrown)
                                .frame(width: 24)
                            Text("お支払い金額")
                                .font(.body)
                            Spacer()
                            Text("¥\(totalAmount)")
                                .font(.headline)
                                .fontWeight(.bold)
                                .foregroundColor(.red)
                        }
                        
                        Divider()
                        
                        HStack {
                            Image(systemName: "calendar")
                                .foregroundColor(.sweetsBrown)
                                .frame(width: 24)
                            Text("配送予定日")
                                .font(.body)
                            Spacer()
                            Text(formatDate(deliveryDate))
                                .font(.body)
                                .foregroundColor(.gray)
                        }
                        
                        HStack {
                            Image(systemName: "clock")
                                .foregroundColor(.sweetsBrown)
                                .frame(width: 24)
                            Text("配送時間帯")
                                .font(.body)
                            Spacer()
                            Text(deliveryTime)
                                .font(.body)
                                .foregroundColor(.gray)
                        }
                    }
                    .padding()
                    .background(Color.white)
                    .cornerRadius(12)
                    .shadow(color: .black.opacity(0.05), radius: 8, x: 0, y: 2)
                }
                .padding(.horizontal)
                .transition(.move(edge: .bottom).combined(with: .opacity))
            }
            
            Spacer()
            
            // Note
            if showDetails {
                VStack(spacing: 12) {
                    Text("※ これはデモ機能です")
                        .font(.caption)
                        .foregroundColor(.gray)
                    Text("実際の決済や配送は行われません")
                        .font(.caption)
                        .foregroundColor(.gray)
                }
                .padding()
                .background(Color.yellow.opacity(0.1))
                .cornerRadius(8)
                .padding(.horizontal)
            }
            
            // Buttons
            if showDetails {
                VStack(spacing: 12) {
                    NavigationLink(destination: OrderHistoryView()) {
                        HStack {
                            Image(systemName: "list.bullet.rectangle.portrait")
                            Text("注文履歴を見る")
                        }
                        .font(.headline)
                        .foregroundColor(.white)
                        .frame(maxWidth: .infinity)
                        .padding()
                        .background(Color.sweetsBrown)
                        .cornerRadius(8)
                    }
                    
                    Button(action: {
                        // Navigate back to home
                        navigateToHome()
                    }) {
                        Text("ホームに戻る")
                            .font(.headline)
                            .foregroundColor(.sweetsBrown)
                            .frame(maxWidth: .infinity)
                            .padding()
                            .background(Color.white)
                            .overlay(
                                RoundedRectangle(cornerRadius: 8)
                                    .stroke(Color.sweetsBrown, lineWidth: 2)
                            )
                            .cornerRadius(8)
                    }
                }
                .padding(.horizontal)
                .padding(.bottom, 20)
            }
        }
        .navigationBarBackButtonHidden(true)
        .background(Color(UIColor.systemGroupedBackground).ignoresSafeArea())
        .onAppear {
            print("🎯 OrderSuccessView が表示されました")
            print("   注文番号: \(orderNumber)")
            print("   合計金額: ¥\(totalAmount)")
            startAnimation()
            
            // Clear cart after animation starts - delay enough to ensure navigation is stable
            DispatchQueue.main.asyncAfter(deadline: .now() + 2.0) {
                print("🗑️ カートをクリア（成功ページ表示中）")
                appState.clearCart()
            }
        }
    }
    
    func startAnimation() {
        print("🎬 OrderSuccessView: アニメーション開始")
        
        // Progress animation (0-1.2 seconds)
        withAnimation(.easeInOut(duration: 1.2)) {
            animationProgress = 1.0
        }
        print("✅ プログレスバーアニメーション開始（1.2秒）")
        
        // Show checkmark after progress completes
        DispatchQueue.main.asyncAfter(deadline: .now() + 1.2) {
            print("✅ チェックマーク表示")
            withAnimation(.spring(response: 0.5, dampingFraction: 0.6)) {
                showCheckmark = true
            }
        }
        
        // Show details slightly after checkmark
        DispatchQueue.main.asyncAfter(deadline: .now() + 1.5) {
            print("✅ 詳細情報表示")
            withAnimation(.easeOut(duration: 0.5)) {
                showDetails = true
            }
        }
    }
    
    func formatDate(_ date: Date) -> String {
        let formatter = DateFormatter()
        formatter.dateFormat = "M月d日 (E)"
        formatter.locale = Locale(identifier: "ja_JP")
        return formatter.string(from: date)
    }
    
    func navigateToHome() {
        // Pop to root view
        if let windowScene = UIApplication.shared.connectedScenes.first as? UIWindowScene,
           let window = windowScene.windows.first,
           let rootViewController = window.rootViewController {
            
            // Find the navigation controller
            var currentVC = rootViewController
            while let presentedVC = currentVC.presentedViewController {
                currentVC = presentedVC
            }
            
            // Dismiss all presented views
            currentVC.dismiss(animated: true)
        }
    }
}

// Preview
struct OrderSuccessView_Previews: PreviewProvider {
    static var previews: some View {
        NavigationView {
            OrderSuccessView(
                orderNumber: "ABC123",
                totalAmount: 2120,
                deliveryDate: Date().addingTimeInterval(86400 * 3),
                deliveryTime: "午前中(8-12時)"
            )
            .environmentObject(AppState())
        }
    }
}
