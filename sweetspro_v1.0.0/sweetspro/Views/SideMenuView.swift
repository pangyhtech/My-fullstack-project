import SwiftUI

struct SideMenuView: View {
    @EnvironmentObject var userManager: UserManager
    @Binding var isShowing: Bool
    
    var body: some View {
        ZStack(alignment: .leading) {
            // 背景遮罩
            if isShowing {
                Color.black.opacity(0.3)
                    .ignoresSafeArea()
                    .onTapGesture {
                        withAnimation {
                            isShowing = false
                        }
                    }
                
                // 侧边栏
                HStack(spacing: 0) {
                    VStack(alignment: .leading, spacing: 0) {
                        // 头部 - 用户信息
                        VStack(alignment: .leading, spacing: 12) {
                            HStack {
                                Image(systemName: "person.circle.fill")
                                    .font(.system(size: 50))
                                    .foregroundColor(.sweetsBrown)
                                
                                VStack(alignment: .leading, spacing: 4) {
                                    Text(userManager.currentUser?.name ?? "ゲスト")
                                        .font(.headline)
                                        .fontWeight(.bold)
                                    
                                    HStack(spacing: 4) {
                                        Text(userManager.currentUser?.membershipTier.rawValue ?? "レギュラー")
                                            .font(.caption)
                                            .padding(.horizontal, 8)
                                            .padding(.vertical, 4)
                                            .background(tierColor())
                                            .foregroundColor(.white)
                                            .cornerRadius(4)
                                        
                                        Text("\(userManager.currentUser?.points ?? 0) pt")
                                            .font(.caption)
                                            .foregroundColor(.sweetsBrown)
                                    }
                                }
                            }
                        }
                        .padding()
                        .background(Color.sweetsLightBg)
                        
                        Divider()
                        
                        // 菜单项
                        ScrollView {
                            VStack(alignment: .leading, spacing: 0) {
                                // 会员系统
                                SideMenuSection(title: "会員特典")
                                
                                SideMenuItem(
                                    icon: "star.fill",
                                    title: "会員ランク・ポイント",
                                    destination: AnyView(MembershipView()),
                                    isShowing: $isShowing
                                )
                                
                                SideMenuItem(
                                    icon: "ticket.fill",
                                    title: "クーポン",
                                    destination: AnyView(MembershipView()),
                                    isShowing: $isShowing
                                )
                                
                                SideMenuItem(
                                    icon: "giftcard.fill",
                                    title: "特典・キャンペーン",
                                    destination: AnyView(Text("特典・キャンペーン").navigationTitle("特典")),
                                    isShowing: $isShowing
                                )
                                
                                Divider()
                                
                                // 購入履歴
                                SideMenuSection(title: "ご利用履歴")
                                
                                SideMenuItem(
                                    icon: "bag.fill",
                                    title: "購入履歴",
                                    destination: AnyView(OrderHistoryView()),
                                    isShowing: $isShowing
                                )
                                
                                SideMenuItem(
                                    icon: "heart.fill",
                                    title: "お気に入り",
                                    badge: userManager.favorites.count > 0 ? "\(userManager.favorites.count)" : nil,
                                    destination: AnyView(FavoritesView()),
                                    isShowing: $isShowing
                                )
                                
                                Divider()
                                
                                // サポート
                                SideMenuSection(title: "サポート")
                                
                                SideMenuItem(
                                    icon: "questionmark.circle",
                                    title: "よくある質問",
                                    destination: AnyView(FAQView()),
                                    isShowing: $isShowing
                                )
                                
                                SideMenuItem(
                                    icon: "envelope",
                                    title: "お問い合わせ",
                                    destination: AnyView(InquiryView()),
                                    isShowing: $isShowing
                                )
                                
                                Divider()
                                
                                // 企業情報・法的情報
                                SideMenuSection(title: "企業情報")
                                
                                SideMenuItem(
                                    icon: "building.2",
                                    title: "会社概要",
                                    destination: AnyView(CompanyInfoView()),
                                    isShowing: $isShowing
                                )
                                
                                Divider()
                                
                                SideMenuSection(title: "法的情報")
                                
                                SideMenuItem(
                                    icon: "doc.text",
                                    title: "利用規約",
                                    destination: AnyView(TermsOfServiceView()),
                                    isShowing: $isShowing
                                )
                                
                                SideMenuItem(
                                    icon: "hand.raised",
                                    title: "プライバシーポリシー",
                                    destination: AnyView(PrivacyPolicyView()),
                                    isShowing: $isShowing
                                )
                                
                                SideMenuItem(
                                    icon: "doc.badge.gearshape",
                                    title: "ライセンス",
                                    destination: AnyView(LicenseView()),
                                    isShowing: $isShowing
                                )
                                
                                SideMenuItem(
                                    icon: "info.circle",
                                    title: "バージョン情報",
                                    destination: AnyView(AppInfoView()),
                                    isShowing: $isShowing
                                )
                            }
                        }
                        
                        Spacer()
                    }
                    .frame(width: UIScreen.main.bounds.width * 0.6)
                    .background(Color.white)
                    .transition(.move(edge: .leading))
                    .gesture(
                        DragGesture()
                            .onEnded { value in
                                if value.translation.width < -50 {  // Swipe left to close
                                    withAnimation {
                                        isShowing = false
                                    }
                                }
                            }
                    )
                    
                    Spacer()
                }
            }
        }
        .animation(.easeInOut(duration: 0.3), value: isShowing)
    }
    
    func tierColor() -> Color {
        switch userManager.currentUser?.membershipTier {
        case .platinum:
            return Color.purple
        case .gold:
            return Color.yellow
        case .silver:
            return Color.gray
        default:
            return Color.blue
        }
    }
}

struct SideMenuSection: View {
    let title: String
    
    var body: some View {
        Text(title)
            .font(.caption)
            .foregroundColor(.gray)
            .padding(.horizontal)
            .padding(.top, 16)
            .padding(.bottom, 8)
    }
}

struct SideMenuItem: View {
    let icon: String
    let title: String
    var badge: String? = nil
    let destination: AnyView
    @Binding var isShowing: Bool
    
    var body: some View {
        NavigationLink(destination: destination) {
            HStack {
                Image(systemName: icon)
                    .font(.system(size: 20))
                    .foregroundColor(.sweetsBrown)
                    .frame(width: 30)
                
                Text(title)
                    .font(.body)
                    .foregroundColor(.black)
                    .multilineTextAlignment(.leading)
                    .lineLimit(2)
                    .fixedSize(horizontal: false, vertical: true)
                
                Spacer()
                
                if let badge = badge {
                    Text(badge)
                        .font(.caption)
                        .padding(.horizontal, 8)
                        .padding(.vertical, 2)
                        .background(Color.red)
                        .foregroundColor(.white)
                        .cornerRadius(10)
                }
                
                Image(systemName: "chevron.right")
                    .font(.caption)
                    .foregroundColor(.gray)
            }
            .padding(.horizontal)
            .padding(.vertical, 12)
        }
        .simultaneousGesture(TapGesture().onEnded {
            withAnimation {
                isShowing = false
            }
        })
    }
}
