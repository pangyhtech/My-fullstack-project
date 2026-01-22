import SwiftUI

struct MyPageView: View {
    @EnvironmentObject var appState: AppState
    @EnvironmentObject var userManager: UserManager
    @State private var email = ""
    @State private var password = ""
    
    var body: some View {
        NavigationView {
            if appState.isLoggedIn {
                List {
                    Section(header: Text("会員情報")) {
                        HStack {
                            Image(systemName: "person.circle.fill")
                                .font(.system(size: 50))
                                .foregroundColor(.gray)
                            VStack(alignment: .leading) {
                                Text(userManager.currentUser?.name ?? "User")
                                    .font(.headline)
                                Text(userManager.currentUser?.email ?? "")
                                    .font(.caption)
                                    .foregroundColor(.gray)
                            }
                        }
                        .padding(.vertical)
                        
                        NavigationLink("会員情報を編集", destination: UserEditView())
                    }
                    
                    Section(header: Text("マイページメニュー")) {
                        NavigationLink(destination: OrderHistoryView()) {
                            Text("購入履歴")
                        }
                        NavigationLink(destination: FavoritesView()) {
                            HStack {
                                Text("お気に入り")
                                Spacer()
                                if !userManager.favorites.isEmpty {
                                    Text("\(userManager.favorites.count)")
                                        .font(.caption)
                                        .padding(4)
                                        .background(Color.red)
                                        .foregroundColor(.white)
                                        .clipShape(Circle())
                                }
                            }
                        }
                        NavigationLink("お届け先住所", destination: Text("登録住所: " + (userManager.currentUser?.address ?? "")))
                    }
                    
                    Section {
                        Button("ログアウト") {
                            appState.logout()
                        }
                        .foregroundColor(.red)
                    }
                }
                .navigationTitle("マイページ")
            } else {
                VStack(spacing: 20) {
                    Image(systemName: "lock.shield")
                        .font(.system(size: 60))
                        .foregroundColor(.sweetsBrown)
                        .padding(.bottom, 20)
                    
                    VStack(spacing: 15) {
                        TextField("メールアドレス", text: $email)
                            .textFieldStyle(RoundedBorderTextFieldStyle())
                            .keyboardType(.emailAddress)
                            .autocapitalization(.none)
                        
                        SecureField("パスワード", text: $password)
                            .textFieldStyle(RoundedBorderTextFieldStyle())
                    }
                    .padding(.horizontal)
                    
                    Button(action: {
                        appState.login(email: email.isEmpty ? "demo@sweets-pro.com" : email)
                    }) {
                        Text("ログイン")
                            .fontWeight(.bold)
                            .foregroundColor(.white)
                            .frame(maxWidth: .infinity)
                            .padding()
                            .background(Color.sweetsBrown)
                            .cornerRadius(8)
                    }
                    .padding(.horizontal)
                    
                    Text("パスワードをお忘れの方はこちら")
                        .font(.caption)
                        .foregroundColor(.blue)
                    
                    Divider()
                        .padding(.vertical)
                    
                    Button(action: {
                        // Mock registration
                        appState.login(email: "newuser@example.com")
                    }) {
                        Text("新規会員登録")
                            .fontWeight(.bold)
                            .foregroundColor(.sweetsBrown)
                            .frame(maxWidth: .infinity)
                            .padding()
                            .overlay(
                                RoundedRectangle(cornerRadius: 8)
                                    .stroke(Color.sweetsBrown, lineWidth: 1)
                            )
                    }
                    .padding(.horizontal)
                }
                .padding()
                .navigationTitle("ログイン")
                .background(Color(UIColor.systemGroupedBackground))
            }
        }
    }
}
