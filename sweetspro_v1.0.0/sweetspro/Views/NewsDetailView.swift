import SwiftUI

struct NewsDetailView: View {
    let newsItem: NewsItem
    
    // Random dummy content generator (Japanese)
    private var randomContent: String {
        let paragraphs = [
            "この文章はダミーです。文字の大きさ、量、字間、行間等を確認するために入れています。この文章はダミーです。文字の大きさ、量、字間、行間等を確認するために入れています。",
            "日頃よりSWEETS PROをご愛顧いただき、誠にありがとうございます。さて、この度弊社では、昨今の原材料費高騰や物流コストの上昇に伴い、誠に不本意ながら商品の価格改定を実施させていただくこととなりました。お客様にはご負担をおかけすることとなり、深くお詫び申し上げますとともに、何卒ご理解いただけますようお願い申し上げます。",
            "新商品「季節のフルーツタルト」の販売を開始いたしました。旬のフルーツをふんだんに使用した、贅沢な一品となっております。ぜひこの機会にご賞味ください。",
            "天候不良の影響により、一部地域への配送に遅延が生じる可能性がございます。お客様には大変ご迷惑をおかけいたしますが、ご了承のほどよろしくお願い申し上げます。",
            "誠に勝手ながら、年末年始の営業は以下の通りとさせていただきます。ご不便をおかけいたしますが、何卒よろしくお願い申し上げます。"
        ]
        // Randomly select 3-5 paragraphs
        let count = Int.random(in: 3...5)
        return paragraphs.shuffled().prefix(count).joined(separator: "\n\n")
    }
    
    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 20) {
                Text(newsItem.date)
                    .font(.subheadline)
                    .foregroundColor(.gray)
                
                Text(newsItem.title)
                    .font(.title2)
                    .fontWeight(.bold)
                    .foregroundColor(.sweetsBrown)
                    .multilineTextAlignment(.leading)
                
                Divider()
                
                Text(randomContent)
                    .font(.body)
                    .lineSpacing(8)
                    .foregroundColor(.black)
                
                Spacer()
            }
            .frame(maxWidth: .infinity, alignment: .leading)
            .padding()
        }
        .navigationBarTitleDisplayMode(.inline)
        .background(Color.white)
    }
}
