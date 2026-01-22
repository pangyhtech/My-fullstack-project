import SwiftUI

struct InquiryView: View {
    @State private var name: String = ""
    @State private var email: String = ""
    @State private var content: String = ""
    @State private var showingAlert = false
    
    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 20) {
                // Header
                VStack(alignment: .leading, spacing: 10) {
                    Text("お問い合わせ")
                        .font(.title2)
                        .fontWeight(.bold)
                        .foregroundColor(.sweetsBrown)
                    Text("ご不明点などございましたら、お気軽にお問い合わせくださいませ。")
                        .font(.caption)
                        .foregroundColor(.gray)
                    Divider()
                }
                
                // Form
                VStack(alignment: .leading, spacing: 15) {
                    Group {
                        Text("お名前")
                            .font(.headline)
                            .foregroundColor(.black)
                        TextField("お名前を入力してください", text: $name)
                            .textFieldStyle(RoundedBorderTextFieldStyle())
                    }
                    
                    Group {
                        Text("メールアドレス")
                            .font(.headline)
                            .foregroundColor(.black)
                        TextField("メールアドレスを入力してください", text: $email)
                            .textFieldStyle(RoundedBorderTextFieldStyle())
                            .keyboardType(.emailAddress)
                            .autocapitalization(.none)
                    }
                    
                    Group {
                        Text("お問い合わせ内容")
                            .font(.headline)
                            .foregroundColor(.black)
                        TextEditor(text: $content)
                            .frame(height: 150)
                            .overlay(RoundedRectangle(cornerRadius: 8).stroke(Color.gray.opacity(0.3), lineWidth: 1))
                    }
                    
                    Button(action: {
                        // Mock submission
                        showingAlert = true
                    }) {
                        Text("確認する")
                            .font(.headline)
                            .foregroundColor(.white)
                            .frame(maxWidth: .infinity)
                            .padding()
                            .background(Color.sweetsBrown)
                            .cornerRadius(8)
                    }
                    .padding(.top, 20)
                    .alert(isPresented: $showingAlert) {
                        Alert(title: Text("送信完了"), message: Text("お問い合わせありがとうございます。（デモ機能のため実際には送信されません）"), dismissButton: .default(Text("OK")))
                    }
                }
            }
            .padding()
        }
        .navigationBarTitleDisplayMode(.inline)
        .background(Color.white)
        .onTapGesture {
            // Dismiss keyboard
            UIApplication.shared.sendAction(#selector(UIResponder.resignFirstResponder), to: nil, from: nil, for: nil)
        }
    }
}
