import SwiftUI

struct CompanyInfoView: View {
    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 20) {
                // Company Logo/Header
                VStack(spacing: 12) {
                    Image(systemName: "building.2.fill")
                        .font(.system(size: 60))
                        .foregroundColor(.sweetsBrown)
                    
                    Text("GOYO FOODS")
                        .font(.title)
                        .fontWeight(.bold)
                    
                    Text("御用フーズ株式会社")
                        .font(.headline)
                        .foregroundColor(.gray)
                }
                .frame(maxWidth: .infinity)
                .padding()
                
                Divider()
                
                // Company Info
                VStack(alignment: .leading, spacing: 16) {
                    InfoRow(title: "会社名", value: "御用フーズ株式会社\nGOYO FOODS CO., LTD.")
                    InfoRow(title: "設立", value: "1985年")
                    InfoRow(title: "本社所在地", value: "東京都渋谷区神宮前1-2-3")
                    InfoRow(title: "事業内容", value: "洋菓子・和菓子の製造販売\nオンライン通販事業")
                    InfoRow(title: "従業員数", value: "約300名")
                }
                .padding()
                
                Divider()
                
                // Website Link
                Link(destination: URL(string: "https://www.goyofoods.co.jp/")!) {
                    HStack {
                        Image(systemName: "globe")
                        Text("公式ウェブサイト")
                        Spacer()
                        Text("www.goyofoods.co.jp")
                            .font(.caption)
                            .foregroundColor(.gray)
                        Image(systemName: "arrow.up.right")
                    }
                    .padding()
                    .background(Color.sweetsLightBg)
                    .cornerRadius(8)
                }
                .padding(.horizontal)
                
                // Social Media (Mock)
                VStack(alignment: .leading, spacing: 12) {
                    Text("SNS")
                        .font(.headline)
                        .padding(.horizontal)
                    
                    HStack(spacing: 20) {
                        SocialButton(icon: "f.square.fill", name: "Facebook")
                        SocialButton(icon: "camera.fill", name: "Instagram")
                        SocialButton(icon: "message.fill", name: "LINE")
                    }
                    .padding(.horizontal)
                }
            }
            .padding(.vertical)
        }
        .navigationTitle("企業情報")
        .navigationBarTitleDisplayMode(.inline)
        .background(Color(UIColor.systemGroupedBackground))
    }
}

struct InfoRow: View {
    let title: String
    let value: String
    
    var body: some View {
        VStack(alignment: .leading, spacing: 4) {
            Text(title)
                .font(.caption)
                .foregroundColor(.gray)
            Text(value)
                .font(.body)
        }
    }
}

struct SocialButton: View {
    let icon: String
    let name: String
    
    var body: some View {
        VStack(spacing: 8) {
            Image(systemName: icon)
                .font(.system(size: 30))
                .foregroundColor(.sweetsBrown)
            Text(name)
                .font(.caption)
        }
        .frame(maxWidth: .infinity)
        .padding()
        .background(Color.white)
        .cornerRadius(8)
    }
}

// Terms of Service
struct TermsOfServiceView: View {
    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 16) {
                Text("利用規約")
                    .font(.title2)
                    .fontWeight(.bold)
                    .padding(.bottom)
                
                Section("第1条（適用）") {
                    Text("本規約は、ユーザーが本サービスをご利用頂く際の一切の行為に適用されるものとします。")
                        .font(.body)
                }
                
                Section("第2条（利用登録）") {
                    Text("登録希望者が当社の定める方法によって利用登録を申請し、当社がこれを承認することによって、利用登録が完了するものとします。")
                        .font(.body)
                }
                
                Section("第3条（ユーザーIDおよびパスワードの管理）") {
                    Text("ユーザーは、自己の責任において、本サービスのユーザーIDおよびパスワードを適切に管理するものとします。")
                        .font(.body)
                }
                
                Section("第4条（禁止事項）") {
                    VStack(alignment: .leading, spacing: 8) {
                        Text("ユーザーは、本サービスの利用にあたり、以下の行為をしてはなりません。")
                        Text("・法令または公序良俗に違反する行為")
                        Text("・犯罪行為に関連する行為")
                        Text("・当社のサーバーまたはネットワークの機能を破壊する行為")
                        Text("・当社のサービスの運営を妨害する行為")
                    }
                    .font(.body)
                }
                
                Section("第5条（本サービスの提供の停止等）") {
                    Text("当社は、以下のいずれかの事由があると判断した場合、ユーザーに事前に通知することなく本サービスの全部または一部の提供を停止または中断することができるものとします。")
                        .font(.body)
                }
                
                Text("最終更新日: 2026年1月22日")
                    .font(.caption)
                    .foregroundColor(.gray)
                    .padding(.top)
            }
            .padding()
        }
        .navigationTitle("利用規約")
        .navigationBarTitleDisplayMode(.inline)
        .background(Color(UIColor.systemGroupedBackground))
    }
}

// Privacy Policy
struct PrivacyPolicyView: View {
    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 16) {
                Text("プライバシーポリシー")
                    .font(.title2)
                    .fontWeight(.bold)
                    .padding(.bottom)
                
                Section("個人情報の収集について") {
                    Text("当社は、ユーザーが本サービスを利用する際に、氏名、メールアドレス、電話番号、住所等の個人情報を収集することがあります。")
                        .font(.body)
                }
                
                Section("個人情報の利用目的") {
                    VStack(alignment: .leading, spacing: 8) {
                        Text("収集した個人情報は、以下の目的で利用いたします。")
                        Text("・本サービスの提供・運営のため")
                        Text("・ユーザーからのお問い合わせに回答するため")
                        Text("・メンテナンス、重要なお知らせなどの連絡のため")
                        Text("・利用規約に違反したユーザーへの対応のため")
                    }
                    .font(.body)
                }
                
                Section("個人情報の第三者への開示") {
                    Text("当社は、次に掲げる場合を除いて、個人情報を第三者に提供することはありません。")
                        .font(.body)
                }
                
                Section("Cookie（クッキー）について") {
                    Text("本サービスでは、ユーザーの利便性向上のためCookieを使用することがあります。")
                        .font(.body)
                }
                
                Section("お問い合わせ窓口") {
                    VStack(alignment: .leading, spacing: 4) {
                        Text("本ポリシーに関するお問い合わせは、下記の窓口までお願いいたします。")
                        Text("メール: privacy@goyofoods.co.jp")
                            .foregroundColor(.blue)
                    }
                    .font(.body)
                }
                
                Text("最終更新日: 2026年1月22日")
                    .font(.caption)
                    .foregroundColor(.gray)
                    .padding(.top)
            }
            .padding()
        }
        .navigationTitle("プライバシーポリシー")
        .navigationBarTitleDisplayMode(.inline)
        .background(Color(UIColor.systemGroupedBackground))
    }
}

// License View
struct LicenseView: View {
    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 16) {
                Text("ライセンス情報")
                    .font(.title2)
                    .fontWeight(.bold)
                    .padding(.bottom)
                
                Section("使用ライブラリ") {
                    LicenseItem(
                        name: "SwiftUI",
                        license: "Apple Inc.",
                        description: "iOS用ユーザーインターフェース構築フレームワーク"
                    )
                    
                    LicenseItem(
                        name: "SF Symbols",
                        license: "Apple Inc.",
                        description: "Appleが提供するアイコンセット"
                    )
                }
                
                Divider()
                
                Section("オープンソースライセンス") {
                    Text("本アプリケーションは、以下のオープンソースソフトウェアを使用しています。")
                        .font(.body)
                        .foregroundColor(.gray)
                }
                
                Text("© 2026 GOYO FOODS CO., LTD. All rights reserved.")
                    .font(.caption)
                    .foregroundColor(.gray)
                    .padding(.top)
            }
            .padding()
        }
        .navigationTitle("ライセンス")
        .navigationBarTitleDisplayMode(.inline)
        .background(Color(UIColor.systemGroupedBackground))
    }
}

struct LicenseItem: View {
    let name: String
    let license: String
    let description: String
    
    var body: some View {
        VStack(alignment: .leading, spacing: 4) {
            Text(name)
                .font(.headline)
            Text(license)
                .font(.caption)
                .foregroundColor(.sweetsBrown)
            Text(description)
                .font(.caption)
                .foregroundColor(.gray)
        }
        .padding()
        .background(Color.white)
        .cornerRadius(8)
    }
}

// App Info View
struct AppInfoView: View {
    var body: some View {
        List {
            Section {
                HStack {
                    Text("バージョン")
                    Spacer()
                    Text("1.0.0")
                        .foregroundColor(.gray)
                }
                
                HStack {
                    Text("ビルド番号")
                    Spacer()
                    Text("2026.01.22")
                        .foregroundColor(.gray)
                }
            }
            
            Section {
                HStack {
                    Text("開発者")
                    Spacer()
                    Text("GOYO FOODS")
                        .foregroundColor(.gray)
                }
                
                HStack {
                    Text("リリース日")
                    Spacer()
                    Text("2026年1月")
                        .foregroundColor(.gray)
                }
            }
            
            Section(header: Text("アプリについて")) {
                Text("SWEETS PROは、御用フーズが提供する洋菓子・和菓子のオンラインショッピングアプリです。厳選されたスイーツを、快適にお買い求めいただけます。")
                    .font(.caption)
                    .foregroundColor(.gray)
            }
        }
        .navigationTitle("バージョン情報")
        .navigationBarTitleDisplayMode(.inline)
    }
}
