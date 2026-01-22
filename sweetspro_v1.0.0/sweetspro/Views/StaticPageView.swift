import SwiftUI

struct StaticPageView: View {
    let title: String
    
    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 20) {
                Text(title)
                    .font(.title2)
                    .fontWeight(.bold)
                    .foregroundColor(.sweetsBrown)
                
                Divider()
                
                Text("""
                    こちらは「\(title)」のサンプルページです。
                    
                    実際のWebサイトでは、ここに詳細な規約やポリシー等の条文が掲載されます。
                    
                    （以下、ダミーテキスト）
                    本規約は、株式会社SWEETS PRO（以下「当社」といいます。）が提供するサービス（以下「本サービス」といいます。）の利用条件を定めるものです。登録ユーザーの皆さま（以下「ユーザー」といいます。）には、本規約に従って、本サービスをご利用いただきます。
                    
                    第1条（適用）
                    本規約は、ユーザーと当社との間の本サービスの利用に関わる一切の関係に適用されるものとします。当社は本サービスに関し、本規約のほか、ご利用にあたってのルール等、各種の定め（以下「個別規定」といいます。）をすることがあります。これら個別規定はその名称のいかんに関わらず、本規約の一部を構成するものとします。
                    """)
                    .font(.body)
                    .foregroundColor(.black)
                    .lineSpacing(5)
                
                Spacer()
            }
            .frame(maxWidth: .infinity, alignment: .leading)
            .padding()
        }
        .navigationBarTitleDisplayMode(.inline)
        .background(Color.white)
    }
}
