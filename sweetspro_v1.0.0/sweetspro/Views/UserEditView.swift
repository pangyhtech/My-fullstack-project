import SwiftUI

struct UserEditView: View {
    @EnvironmentObject var userManager: UserManager
    @Environment(\.presentationMode) var presentationMode
    
    @State private var name: String = ""
    @State private var email: String = ""
    @State private var phoneNumber: String = ""
    @State private var postalCode: String = ""
    @State private var address: String = ""
    @State private var showSaveAlert = false
    
    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 20) {
                Text("会員情報編集")
                    .font(.title2)
                    .fontWeight(.bold)
                    .foregroundColor(.sweetsBrown)
                
                Divider()
                
                VStack(alignment: .leading, spacing: 15) {
                    // User ID (read-only)
                    VStack(alignment: .leading, spacing: 8) {
                        Text("会員ID")
                            .font(.headline)
                        Text(userManager.currentUser?.id ?? "")
                            .font(.body)
                            .foregroundColor(.gray)
                            .padding(12)
                            .frame(maxWidth: .infinity, alignment: .leading)
                            .background(Color.gray.opacity(0.1))
                            .cornerRadius(8)
                    }
                    
                    // Name
                    VStack(alignment: .leading, spacing: 8) {
                        Text("お名前 *")
                            .font(.headline)
                        TextField("お名前", text: $name)
                            .textFieldStyle(RoundedBorderTextFieldStyle())
                    }
                    
                    // Email
                    VStack(alignment: .leading, spacing: 8) {
                        Text("メールアドレス *")
                            .font(.headline)
                        TextField("メールアドレス", text: $email)
                            .textFieldStyle(RoundedBorderTextFieldStyle())
                            .keyboardType(.emailAddress)
                            .autocapitalization(.none)
                    }
                    
                    // Phone Number
                    VStack(alignment: .leading, spacing: 8) {
                        Text("電話番号")
                            .font(.headline)
                        TextField("090-1234-5678", text: $phoneNumber)
                            .textFieldStyle(RoundedBorderTextFieldStyle())
                            .keyboardType(.phonePad)
                    }
                    
                    // Postal Code
                    VStack(alignment: .leading, spacing: 8) {
                        Text("郵便番号")
                            .font(.headline)
                        TextField("150-0001", text: $postalCode)
                            .textFieldStyle(RoundedBorderTextFieldStyle())
                            .keyboardType(.numberPad)
                    }
                    
                    // Address
                    VStack(alignment: .leading, spacing: 8) {
                        Text("住所")
                            .font(.headline)
                        TextEditor(text: $address)
                            .frame(height: 80)
                            .overlay(
                                RoundedRectangle(cornerRadius: 8)
                                    .stroke(Color.gray.opacity(0.3), lineWidth: 1)
                            )
                    }
                    
                    // Save Button
                    Button(action: {
                        userManager.updateUserInfo(
                            name: name,
                            email: email,
                            phoneNumber: phoneNumber,
                            postalCode: postalCode,
                            address: address
                        )
                        showSaveAlert = true
                    }) {
                        Text("保存")
                            .font(.headline)
                            .foregroundColor(.white)
                            .frame(maxWidth: .infinity)
                            .padding()
                            .background(Color.sweetsBrown)
                            .cornerRadius(8)
                    }
                    .padding(.top, 20)
                    .alert(isPresented: $showSaveAlert) {
                        Alert(
                            title: Text("保存完了"),
                            message: Text("会員情報を更新しました"),
                            dismissButton: .default(Text("OK")) {
                                presentationMode.wrappedValue.dismiss()
                            }
                        )
                    }
                }
            }
            .padding()
        }
        .navigationBarTitleDisplayMode(.inline)
        .background(Color.white)
        .onAppear {
            loadUserData()
        }
    }
    
    func loadUserData() {
        guard let user = userManager.currentUser else { return }
        name = user.name
        email = user.email
        phoneNumber = user.phoneNumber
        postalCode = user.postalCode
        address = user.address
    }
}
