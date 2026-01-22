import SwiftUI

struct MembershipView: View {
    @EnvironmentObject var userManager: UserManager
    @EnvironmentObject var couponManager: CouponManager
    
    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 20) {
                // Membership Card
                MembershipCardView(user: userManager.currentUser)
                    .padding(.horizontal)
                    .padding(.top)
                
                // Points Section
                VStack(alignment: .leading, spacing: 12) {
                    Text("ポイント")
                        .font(.headline)
                    
                    HStack {
                        VStack(alignment: .leading) {
                            Text("現在のポイント")
                                .font(.caption)
                                .foregroundColor(.gray)
                            Text("\(userManager.currentUser?.points ?? 0) pt")
                                .font(.title2)
                                .fontWeight(.bold)
                                .foregroundColor(.sweetsBrown)
                        }
                        Spacer()
                        VStack(alignment: .trailing) {
                            Text("累計購入金額")
                                .font(.caption)
                                .foregroundColor(.gray)
                            Text("¥\(userManager.currentUser?.totalSpent ?? 0)")
                                .font(.title3)
                                .fontWeight(.semibold)
                        }
                    }
                    .padding()
                    .background(Color.white)
                    .cornerRadius(8)
                }
                .padding(.horizontal)
                
                // Next Tier Progress
                if let nextTier = getNextTier() {
                    NextTierProgressView(currentPoints: userManager.currentUser?.points ?? 0, nextTier: nextTier)
                        .padding(.horizontal)
                }
                
                Divider().padding(.vertical)
                
                // Coupons Section
                VStack(alignment: .leading, spacing: 12) {
                    Text("利用可能なクーポン")
                        .font(.headline)
                        .padding(.horizontal)
                    
                    ForEach(couponManager.getAvailableCoupons()) { coupon in
                        CouponCardView(coupon: coupon)
                            .padding(.horizontal)
                    }
                }
            }
            .padding(.bottom)
        }
        .navigationTitle("会員特典")
        .navigationBarTitleDisplayMode(.inline)
        .background(Color(UIColor.systemGroupedBackground))
    }
    
    func getNextTier() -> MembershipTier? {
        guard let current = userManager.currentUser?.membershipTier else { return nil }
        
        switch current {
        case .regular: return .silver
        case .silver: return .gold
        case .gold: return .platinum
        case .platinum: return nil
        }
    }
}

struct MembershipCardView: View {
    let user: SweetsUser?
    
    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            HStack {
                Text(user?.membershipTier.rawValue ?? "レギュラー")
                    .font(.title2)
                    .fontWeight(.bold)
                    .foregroundColor(.white)
                Spacer()
                Image(systemName: "star.fill")
                    .font(.title)
                    .foregroundColor(.white)
            }
            
            Text(user?.name ?? "")
                .font(.headline)
                .foregroundColor(.white)
            
            Text("会員ID: \(user?.id.prefix(8) ?? "")")
                .font(.caption)
                .foregroundColor(.white.opacity(0.8))
            
            HStack {
                Text("割引率")
                    .font(.caption)
                    .foregroundColor(.white.opacity(0.8))
                Spacer()
                Text("\(Int((user?.membershipTier.discountRate ?? 0) * 100))% OFF")
                    .font(.headline)
                    .foregroundColor(.white)
            }
        }
        .padding()
        .background(
            LinearGradient(
                colors: tierColors(),
                startPoint: .topLeading,
                endPoint: .bottomTrailing
            )
        )
        .cornerRadius(12)
        .shadow(radius: 4)
    }
    
    func tierColors() -> [Color] {
        switch user?.membershipTier {
        case .platinum:
            return [Color.purple, Color.purple.opacity(0.7)]
        case .gold:
            return [Color.yellow, Color.orange]
        case .silver:
            return [Color.gray, Color.gray.opacity(0.7)]
        default:
            return [Color.blue, Color.blue.opacity(0.7)]
        }
    }
}

struct NextTierProgressView: View {
    let currentPoints: Int
    let nextTier: MembershipTier
    
    var progress: Double {
        return Double(currentPoints) / Double(nextTier.requiredPoints)
    }
    
    var pointsNeeded: Int {
        return max(0, nextTier.requiredPoints - currentPoints)
    }
    
    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            Text("次のランクまで")
                .font(.headline)
            
            HStack {
                Text(nextTier.rawValue)
                    .font(.subheadline)
                    .foregroundColor(.sweetsBrown)
                Spacer()
                Text("\(pointsNeeded) pt")
                    .font(.caption)
                    .foregroundColor(.gray)
            }
            
            ProgressView(value: min(progress, 1.0))
                .tint(.sweetsBrown)
        }
        .padding()
        .background(Color.white)
        .cornerRadius(8)
    }
}

struct CouponCardView: View {
    let coupon: Coupon
    
    var body: some View {
        HStack {
            VStack(alignment: .leading, spacing: 4) {
                Text(coupon.title)
                    .font(.headline)
                    .foregroundColor(.sweetsBrown)
                
                if coupon.discountType == .percentage {
                    Text("\(coupon.discountValue)% OFF")
                        .font(.title3)
                        .fontWeight(.bold)
                        .foregroundColor(.red)
                } else {
                    Text("¥\(coupon.discountValue) OFF")
                        .font(.title3)
                        .fontWeight(.bold)
                        .foregroundColor(.red)
                }
                
                if coupon.minPurchase > 0 {
                    Text("¥\(coupon.minPurchase)以上のご購入で利用可")
                        .font(.caption)
                        .foregroundColor(.gray)
                }
                
                Text("有効期限: \(formatDate(coupon.expiryDate))")
                    .font(.caption)
                    .foregroundColor(.gray)
            }
            
            Spacer()
            
            VStack {
                Text(coupon.code)
                    .font(.caption)
                    .fontWeight(.bold)
                    .padding(8)
                    .background(Color.sweetsBrown.opacity(0.1))
                    .cornerRadius(4)
                
                if coupon.isUsed {
                    Text("使用済")
                        .font(.caption)
                        .foregroundColor(.gray)
                }
            }
        }
        .padding()
        .background(Color.white)
        .cornerRadius(8)
        .overlay(
            RoundedRectangle(cornerRadius: 8)
                .stroke(Color.sweetsBrown.opacity(0.3), style: StrokeStyle(lineWidth: 1, dash: [5]))
        )
    }
    
    func formatDate(_ isoString: String) -> String {
        let formatter = ISO8601DateFormatter()
        guard let date = formatter.date(from: isoString) else { return "" }
        let displayFormatter = DateFormatter()
        displayFormatter.dateFormat = "yyyy/MM/dd"
        return displayFormatter.string(from: date)
    }
}
