import SwiftUI

struct FAQView: View {
    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 30) {
                // Header
                VStack(alignment: .leading, spacing: 10) {
                    Text("よくあるご質問")
                        .font(.title2)
                        .fontWeight(.bold)
                        .foregroundColor(.sweetsBrown)
                    Divider()
                }
                
                // Section: Delivery
                VStack(alignment: .leading, spacing: 10) {
                    Text("お届け・送料について")
                        .font(.headline)
                        .foregroundColor(.sweetsBrown)
                        .padding(.top)
                    
                    FAQItem(question: "配送業者について", answer: "【業者】佐川急便\n【配送サービス】飛脚クール便（冷凍）\n※離島（佐川急便エリア外）への配送は、ヤマト運輸の「クール宅急便（冷凍）」になります。")
                    
                    FAQItem(question: "送料について", answer: "配送先1箇所につき、10,000円(税込)以上のご購入で送料無料です。\n※北海道・沖縄は、別途500円の送料になります。")
                    
                    FAQItem(question: "最短でのお届けについて", answer: "最短でのお届けをご希望の場合は、配送希望日を「指定なし」にしてください。\n※明日着（即日発送）は対応できかねます。\n営業日14:59までのご注文は翌営業日発送、15:00以降は翌々営業日発送となります。")
                }

                // Section: Payment
                VStack(alignment: .leading, spacing: 10) {
                    Text("お支払いについて")
                        .font(.headline)
                        .foregroundColor(.sweetsBrown)
                        .padding(.top)
                    
                    FAQItem(question: "利用可能な決済方法は？", answer: "以下の決済方法がご利用いただけます。\n・クレジットカード（JCB, VISA, MASTER, Diners, AMEX）\n・代金引換（手数料330円）\n・Amazon Pay\n・PayPay\n・DSK後払い")
                    
                    FAQItem(question: "クレジットカードの手数料は？", answer: "手数料は無料です。\n※セキュリティ強化のため「EMV 3-Dセキュア」を導入しています。")
                }
                
                // Section: Other
                Group {
                    FAQItem(question: "注文内容を変更できますか？", answer: """
マイページの購入履歴にて、注文状況が「注文済み」に限り、以下項目の変更が可能です。
①配送希望日時　②納品書同梱希望の有無　③のし希望の有無　④領収書希望有無（宛名、但し書き）
※④については、支払方法がクレジット、AmazonPay、PayPayに限ります。
※その他変更をご希望の場合は、お問い合わせください。
変更をご希望な場合は、「マイページ > 購入履歴一覧 > 購入履歴詳細」より変更してください。
""")
                    
                    FAQItem(question: "キャンセルできますか？", answer: """
誠に恐れ入りますが、お客様都合によるご注文後のキャンセルはできません。
ご注文内容は、完了前に必ずご確認いただけますようお願いいたします。
""")
                    
                    FAQItem(question: "領収書を発行できますか？インボイス制度の対応は？", answer: """
現在全ての決済方法に対し、インボイス制度に適応した「電子領収書」を発行しています。
※領収書が不要な方は、お手数ですがお支払い方法画面で「希望しない」を選択してください。
""")
                    
                    FAQItem(question: "最短到着日を教えてください。", answer: """
お客さまの注文日時によって、最短の到着日が異なります。
詳しくは配送・送料についてのページをご覧ください。
""")
                    
                    FAQItem(question: "登録したメールアドレスを忘れました。どうすれば良いですか？", answer: """
お手数をお掛けしますが、お問い合わせよりご連絡ください。
""")
                }
                
                
                // Section: Account & Others
                VStack(alignment: .leading, spacing: 10) {
                    Text("その他")
                        .font(.headline)
                        .foregroundColor(.sweetsBrown)
                        .padding(.top)
                    FAQItem(question: "パスワードを忘れました。どうすれば良いですか？", answer: """
パスワードを再設定していただくことになります。パスワードリマインダーのページから再設定をおこなってください。
""")
                    
                    FAQItem(question: "キャンドルやフォーク、ショッパー等は用意してもらえますか？", answer: """
大変申し訳ございませんが、対応しておりません。
""")
                    
                    FAQItem(question: "熨斗、ギフト包装の対応はできますか？", answer: """
ギフト包装は行っておりません。オリジナル熨斗シール(無料)をご利用いただけます。
""")
                }
            }
            .padding()
        }
        .navigationBarTitleDisplayMode(.inline)
        .background(Color(UIColor.systemGroupedBackground))
    }
}

struct FAQItem: View {
    let question: String
    let answer: String
    @State private var isExpanded: Bool = false
    
    var body: some View {
        VStack(alignment: .leading, spacing: 10) {
            Button(action: {
                withAnimation {
                    isExpanded.toggle()
                }
            }) {
                HStack(alignment: .top) {
                    Text("Q.")
                        .font(.headline)
                        .foregroundColor(.sweetsBrown)
                    
                    Text(question)
                        .font(.headline)
                        .foregroundColor(.black)
                        .multilineTextAlignment(.leading)
                    
                    Spacer()
                    
                    Image(systemName: isExpanded ? "chevron.up" : "chevron.down")
                        .foregroundColor(.gray)
                }
            }
            
            if isExpanded {
                HStack(alignment: .top) {
                    Text("A.")
                        .font(.headline)
                        .foregroundColor(.red)
                    
                    Text(answer)
                        .font(.body)
                        .foregroundColor(.black.opacity(0.8))
                        .padding(.bottom, 5)
                }
                .padding(.top, 5)
            }
            
            Divider()
        }
        .background(Color(UIColor.systemGroupedBackground)) // Tappable area fix
    }
}
