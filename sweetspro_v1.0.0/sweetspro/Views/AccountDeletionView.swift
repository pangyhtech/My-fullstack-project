import SwiftUI

struct AccountDeletionView: View {
    @EnvironmentObject var userManager: UserManager
    @EnvironmentObject var appState: AppState
    @Environment(\.presentationMode) var presentationMode
    
    @State private var confirmText = ""
    @State private var showAlert = false
    @State private var isDeleting = false
    
    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 20) {
                // Warning Section
                VStack(alignment: .leading, spacing: 12) {
                    HStack {
                        Image(systemName: "exclamationmark.triangle.fill")
                            .foregroundColor(.red)
                        Text("アカウント削除")
                            .font(.title2)
                            .fontWeight(.bold)
                            .foregroundColor(.red)
                    }
                    
                    Text("この操作は取り消しできません")
                        .font(.headline)
                        .foregroundColor(.red)
                }
                
                Divider()
                
                // What will be deleted
                VStack(alignment: .leading, spacing: 12) {
                    Text("削除される情報")
                        .font(.headline)
                    
                    DeletionInfoRow(icon: "person.fill", text: "会員情報（氏名、住所、電話番号）")
                    DeletionInfoRow(icon: "bag.fill", text: "購入履歴")
                    DeletionInfoRow(icon: "heart.fill", text: "お気に入り商品")
                    DeletionInfoRow(icon: "star.fill", text: "ポイント・会員ランク")
                    DeletionInfoRow(icon: "ticket.fill", text: "保有クーポン")
                }
                .padding()
                .background(Color.red.opacity(0.1))
                .cornerRadius(8)
                
                Divider()
                
                // Confirmation
                VStack(alignment: .leading, spacing: 12) {
                    Text("確認")
                        .font(.headline)
                    
                    Text("アカウントを削除するには、下記に「削除」と入力してください")
                        .font(.body)
                        .foregroundColor(.gray)
                    
                    TextField("削除", text: $confirmText)
                        .textFieldStyle(RoundedBorderTextFieldStyle())
                }
                
                // Delete Button
                Button(action: {
                    showAlert = true
                }) {
                    if isDeleting {
                        ProgressView()
                            .progressViewStyle(CircularProgressViewStyle(tint: .white))
                            .frame(maxWidth: .infinity)
                            .padding()
                    } else {
                        Text("アカウントを削除する")
                            .font(.headline)
                            .foregroundColor(.white)
                            .frame(maxWidth: .infinity)
                            .padding()
                    }
                }
                .background(confirmText == "削除" ? Color.red : Color.gray)
                .cornerRadius(8)
                .disabled(confirmText != "削除" || isDeleting)
                .padding(.top)
                .alert(isPresented: $showAlert) {
                    Alert(
                        title: Text("最終確認"),
                        message: Text("本当にアカウントを削除しますか？\nこの操作は取り消しできません。"),
                        primaryButton: .destructive(Text("削除")) {
                            deleteAccount()
                        },
                        secondaryButton: .cancel(Text("キャンセル"))
                    )
                }
            }
            .padding()
        }
        .navigationTitle("アカウント削除")
        .navigationBarTitleDisplayMode(.inline)
        .background(Color(UIColor.systemGroupedBackground))
    }
    
    func deleteAccount() {
        isDeleting = true
        
        // Call backend API to delete account
        guard let userId = userManager.currentUser?.id else { return }
        
        let url = URL(string: "http://localhost:8080/api/users/\(userId)")!
        var request = URLRequest(url: url)
        request.httpMethod = "DELETE"
        
        URLSession.shared.dataTask(with: request) { _, response, error in
            DispatchQueue.main.async {
                isDeleting = false
                
                if let _ = error {
                    // Handle error
                    return
                }
                
                // Success - clear local data and logout
                userManager.deleteAccount()
                appState.logout()
                presentationMode.wrappedValue.dismiss()
            }
        }.resume()
    }
}

struct DeletionInfoRow: View {
    let icon: String
    let text: String
    
    var body: some View {
        HStack(spacing: 12) {
            Image(systemName: icon)
                .foregroundColor(.red)
                .frame(width: 24)
            Text(text)
                .font(.body)
        }
    }
}
