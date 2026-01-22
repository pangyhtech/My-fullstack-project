import Foundation

struct Banner: Identifiable {
    let id = UUID()
    let imageUrl: String
    let title: String
}

struct Product: Identifiable {
    let id = UUID()
    let name: String
    let price: Int
    let imageUrl: String
    let badge: String?
    let category: String
    let description: String
    let images: [String]
    let details: ProductDetails?
    
    // Init for simple listing
    init(name: String, price: Int, imageUrl: String, badge: String? = nil, category: String = "General") {
        self.name = name
        self.price = price
        self.imageUrl = imageUrl
        self.badge = badge
        self.category = category
        self.description = "Delicious cake from Sweets Pro."
        self.images = [imageUrl]
        self.details = nil
    }
    
    // Init for detailed product
    init(name: String, price: Int, imageUrl: String, badge: String? = nil, category: String, description: String, images: [String], details: ProductDetails?) {
        self.name = name
        self.price = price
        self.imageUrl = imageUrl
        self.badge = badge
        self.category = category
        self.description = description
        self.images = images
        self.details = details
    }
}

struct ProductDetails {
    let ingredients: String
    let nutrition: String
    let expiration: String
    let storage: String
}

struct NewsItem: Identifiable {
    let id = UUID()
    let date: String
    let title: String
}

struct Category: Identifiable {
    let id = UUID()
    let name: String
    let englishName: String
}

struct MockData {
    static let categories: [Category] = [
        Category(name: "チーズケーキ", englishName: "Cheesecake"),
        Category(name: "チョコレートケーキ", englishName: "Chocolate Cake"),
        Category(name: "モンブラン", englishName: "Mont Blanc"),
        Category(name: "ムースケーキ", englishName: "Mousse Cake"),
        Category(name: "フルーツケーキ", englishName: "Fruit Cake"),
        Category(name: "ティラミス", englishName: "Tiramisu"),
        Category(name: "ショートケーキ", englishName: "Shortcake"),
        Category(name: "セット商品", englishName: "Set Items")
    ]
    
    static let banners: [Banner] = [
        Banner(imageUrl: "https://www.sweets-pro.com/Contents/dist/img/top_slider/2026/top_slider_itoroll.jpg", title: "Ito Roll"),
        Banner(imageUrl: "https://www.sweets-pro.com/Contents/dist/img/top_slider/top_slider_13.jpg", title: "Professional"),
        Banner(imageUrl: "https://www.sweets-pro.com/Contents/dist/img/top_slider/2026/top_slider_icecake.jpg", title: "Ice Cake"),
        Banner(imageUrl: "https://www.sweets-pro.com/Contents/dist/img/top_slider/2026/top_slider_whitedeco.jpg", title: "White Deco"),
        Banner(imageUrl: "https://www.sweets-pro.com/Contents/dist/img/top_slider/2026/top_slider_bergychoco.jpg", title: "Bergy Choco")
    ]
    
    // Detailed Products
    static let cheeseCakeDetail = Product(
        name: "ベイクドチーズケーキ6号12ｶｯﾄ12個入",
        price: 2150,
        imageUrl: "https://www.sweets-pro.com/Contents/ProductSubImages/0/01015760_sub01_LL.jpg",
        badge: "Best Seller",
        category: "チーズケーキ",
        description: "クリームチーズを約60%配合した生地を、じっくり湯煎で焼き上げました。しっとりなめらかなくちどけと、濃厚なクリームチーズの余韻が贅沢な一品。チーズの旨味をシンプルに表現した、また一口食べたくなるロングセラー商品です。",
        images: [
            "https://www.sweets-pro.com/Contents/ProductSubImages/0/01015760_sub01_LL.jpg",
            "https://www.sweets-pro.com/Contents/ProductSubImages/0/01015760_sub02_LL.jpg",
            "https://www.sweets-pro.com/Contents/ProductSubImages/0/01015760_sub03_LL.jpg",
            "https://www.sweets-pro.com/Contents/ProductSubImages/0/01015760_sub04_LL.jpg"
        ],
        details: ProductDetails(
            ingredients: "ナチュラルチーズ（オーストラリア製造又はニュージーランド製造）、液卵、砂糖、マーガリン、小麦粉、コーンスターチ、食用乳化油脂、加糖卵黄、麦芽糖、水あめ、乳等を主要原料とする食品／トレハロース、乳化剤、（一部に小麦・卵・乳成分を含む）",
            nutrition: "1個40gあたり：エネルギー 138kcal、タンパク質 2.7g、脂質 9.4g、炭水化物 10.6g",
            expiration: "冷凍保存で約3ヶ月（推奨）、解凍後は冷蔵で1〜2日",
            storage: "冷凍（-18℃以下）で保存してください"
        )
    )
    
    static let montBlancDetail = Product(
        name: "黒ゴマモンブラン（4個入）※ピック付き",
        price: 1320,
        imageUrl: "https://www.sweets-pro.com/Contents/ProductSubImages/0/01046880_sub01_LL.jpg",
        badge: "No.1",
        category: "モンブラン",
        description: "モンブランクリームとスポンジに、黒ゴマペーストをふんだんに使用しました。一口食べると黒ゴマ本来の香りが広がり、コク深い味わいがお楽しみいただけます。ごまスイーツ好きには堪らない、芳ばしい黒ゴマ風味の和モンブランです。",
        images: [
            "https://www.sweets-pro.com/Contents/ProductSubImages/0/01046880_sub01_LL.jpg",
            "https://www.sweets-pro.com/Contents/ProductSubImages/0/01046880_sub02_LL.jpg",
            "https://www.sweets-pro.com/Contents/ProductSubImages/0/01046880_sub03_LL.jpg"
        ],
        details: ProductDetails(
            ingredients: "白あん（国内製造）、ホイップクリーム、カスタード、ごま、液卵、小麦粉、砂糖、食用乳化油脂、水あめ、麦芽糖、食塩／トレハロース、乳化剤、香料、ｐＨ調整剤、増粘多糖類、（一部に小麦・卵・乳成分・ごま・大豆を含む）",
            nutrition: "1個60gあたり：エネルギー 189kcal、タンパク質 3.4g、脂質 10.1g、炭水化物 21.7g",
            expiration: "冷凍保存で約3ヶ月（推奨）",
            storage: "冷凍（-18℃以下）で保存してください"
        )
    )
    
    static let chocoCakeDetail = Product(
        name: "生チョコケーキ6号12ｶｯﾄ12個入",
        price: 1970,
        imageUrl: "https://www.sweets-pro.com/Contents/ProductSubImages/0/p022_sub01_LL.jpg",
        badge: "Recommended",
        category: "チョコレートケーキ",
        description: "生チョコと練乳を配合した「濃厚な生チョコクリーム」をココアスポンジにサンド＆コーティング。ココアパウダーをたっぷり振りかけ、スポンジからクリームまでチョコ尽くし！",
        images: [
            "https://www.sweets-pro.com/Contents/ProductSubImages/0/p022_sub01_LL.jpg",
            "https://www.sweets-pro.com/Contents/ProductSubImages/0/p022_sub02_LL.jpg",
            "https://www.sweets-pro.com/Contents/ProductSubImages/0/p022_sub03_LL.jpg"
        ],
        details: ProductDetails(
            ingredients: "液卵（国内製造又はタイ製造）、チョコレートホイップクリーム、ホイップクリーム、砂糖、小麦粉、チョコレート、食用乳化油脂、ココアパウダー、水あめ、加糖練乳、乳等を主要原料とする食品、麦芽糖、調整ココア／乳化剤、香料",
            nutrition: "1個30gあたり：エネルギー 98kcal、タンパク質 1.5g、脂質 5.9g、炭水化物 9.6g",
            expiration: "冷凍保存で約3ヶ月（推奨）",
            storage: "冷凍（-18℃以下）で保存してください"
        )
    )
    
    static let fruitCakeDetail = Product(
        name: "彩りフルーツのタルト 5号",
        price: 3200,
        imageUrl: "http://localhost:8080/images/fruit_tart_cake.png",
        badge: "Seasonal",
        category: "フルーツケーキ",
        description: "季節のフルーツをふんだんに使用した贅沢なタルトです。サクサクのタルト生地とカスタードクリームの相性は抜群。いちご、キウイ、ブルーベリー、オレンジなど色とりどりのフレッシュフルーツを美しく飾りました。",
        images: ["http://localhost:8080/images/fruit_tart_cake.png"],
        details: ProductDetails(
            ingredients: "小麦粉（国内製造）、フルーツ（いちご、キウイ、ブルーベリー、オレンジ）、牛乳、バター、砂糖、卵、カスタードクリーム、ゼラチン、ナパージュ／増粘剤、香料、（一部に小麦・卵・乳成分を含む）",
            nutrition: "100gあたり：エネルギー 245kcal、タンパク質 3.8g、脂質 12.5g、炭水化物 29.6g",
            expiration: "冷蔵保存で製造日より3日、解凍後は当日中にお召し上がりください",
            storage: "冷蔵（10℃以下）で保存してください"
        )
    )
    
    static let shortCakeDetail = Product(
        name: "北海道生クリームのショートケーキ",
        price: 3800,
        imageUrl: "http://localhost:8080/images/hokkaido_shortcake.png",
        category: "ショートケーキ",
        description: "北海道産の極上生クリームを使用した、シンプルかつ王道のショートケーキ。ふわふわのスポンジケーキに新鮮な苺をサンドし、なめらかな生クリームで丁寧にデコレーション。スポンジの口溶けと生クリームのコクのバランスにこだわりました。",
        images: ["http://localhost:8080/images/hokkaido_shortcake.png"],
        details: ProductDetails(
            ingredients: "生クリーム（北海道産）（国内製造）、液卵、砂糖、小麦粉、苺、バター、牛乳、水あめ／トレハロース、乳化剤、膨張剤、香料、（一部に小麦・卵・乳成分を含む）",
            nutrition: "100gあたり：エネルギー 328kcal、タンパク質 4.2g、脂質 18.7g、炭水化物 35.1g",
            expiration: "冷蔵保存で製造日より2日、解凍後は当日中にお召し上がりください",
            storage: "冷蔵（10℃以下）で保存してください"
        )
    )
    
    static let setItemDetail = Product(
        name: "人気ケーキ3種食べ比べセット",
        price: 2980,
        imageUrl: "http://localhost:8080/images/cake_assortment_set.png",
        badge: "Gift",
        category: "セット商品",
        description: "当店人気のベイクドチーズケーキ、生チョコケーキ、黒ゴマモンブランの3種類が一度に楽しめる贅沢なセット。それぞれの個性豊かな味わいを食べ比べできます。ギフトボックス入りでプレゼントにも最適です。",
        images: ["http://localhost:8080/images/cake_assortment_set.png"],
        details: ProductDetails(
            ingredients: "各商品の原材料をご参照ください（チーズケーキ、チョコケーキ、モンブランの詰め合わせ）",
            nutrition: "商品により異なります。各商品の栄養成分表示をご参照ください",
            expiration: "冷凍保存で約3ヶ月（推奨）",
            storage: "冷凍（-18℃以下）で保存してください"
        )
    )
    
    
    // Aggregated Arrays
    static let rankingProducts: [Product] = [montBlancDetail, cheeseCakeDetail, chocoCakeDetail]
    
    static let strawberryMontBlanc = Product(
        name: "あまおう苺のモンブラン (4個入)",
        price: 1480,
        imageUrl: "http://localhost:8080/images/strawberry_montblanc_cake.png",
        badge: "NEW",
        category: "モンブラン",
        description: "福岡県産あまおう苺を贅沢に使用した春限定のモンブラン。甘酸っぱい苺の風味とクリーミーなモンブランクリームが絶妙にマッチした逸品です。",
        images: ["http://localhost:8080/images/strawberry_montblanc_cake.png"],
        details: ProductDetails(
            ingredients: "苺ピューレ（国内製造）、ホイップクリーム、カスタード、砂糖、液卵、小麦粉、バター、食用乳化油脂、水あめ、麦芽糖／トレハロース、乳化剤、香料、着色料（紅麹）、（一部に小麦・卵・乳成分を含む）",
            nutrition: "1個55gあたり：エネルギー 168kcal、タンパク質 2.9g、脂質 9.2g、炭水化物 18.5g",
            expiration: "冷凍保存で約3ヶ月（推奨）",
            storage: "冷凍（-18℃以下）で保存してください"
        )
    )
    
    static let pistachioMousse = Product(
        name: "ピスタチオムース",
        price: 1550,
        imageUrl: "http://localhost:8080/images/pistachio_mousse_cake.png",
        badge: "NEW",
        category: "ムースケーキ",
        description: "上質なピスタチオペーストを使用したなめらかなムースケーキ。鮮やかなグリーンと芳醇なナッツの風味が特徴です。ミラーグラーズ仕上げで高級感のある一品。",
        images: ["http://localhost:8080/images/pistachio_mousse_cake.png"],
        details: ProductDetails(
            ingredients: "ピスタチオペースト（イタリア製造）、生クリーム、砂糖、牛乳、ゼラチン、卵白、バター、小麦粉、ナパージュ／乳化剤、香料、着色料（クチナシ）、（一部に小麦・卵・乳成分・ナッツ類を含む）",
            nutrition: "100gあたり：エネルギー 298kcal、タンパク質 5.1g、脂質 19.8g、炭水化物 24.3g",
            expiration: "冷凍保存で約3ヶ月（推奨）",
            storage: "冷凍（-18℃以下）で保存してください"
        )
    )
    
    static let matchaTiramisu = Product(
        name: "宇治抹茶ティラミス",
        price: 1620,
        imageUrl: "http://localhost:8080/images/matcha_tiramisu_dessert.png",
        badge: "Limited",
        category: "ティラミス",
        description: "京都宇治産の最高級抹茶を使用した和風ティラミス。抹茶の豊かな香りとマスカルポーネチーズのコクが絶妙に調和。ほろ苦さと甘みのバランスが絶品です。",
        images: ["http://localhost:8080/images/matcha_tiramisu_dessert.png"],
        details: ProductDetails(
            ingredients: "マスカルポーネチーズ（イタリア製造）、抹茶（宇治産）、生クリーム、砂糖、卵黄、スポンジケーキ、コーヒー、ゼラチン／乳化剤、香料、（一部に小麦・卵・乳成分を含む）",
            nutrition: "1個85gあたり：エネルギー 212kcal、タンパク質 4.3g、脂質 14.1g、炭水化物 17.8g",
            expiration: "冷凍保存で約3ヶ月（推奨）",
            storage: "冷凍（-18℃以下）で保存してください"
        )
    )
    
    static let rareCheesecake = Product(
        name: "レアチーズケーキ 5号",
        price: 2800,
        imageUrl: "http://localhost:8080/images/rare_cheesecake_slice.png",
        category: "チーズケーキ",
        description: "オーストラリア産クリームチーズを使用したなめらかな口当たりのレアチーズケーキ。レモンの爽やかな酸味がアクセント。グラハムクラッカーの香ばしい土台との相性も抜群です。",
        images: ["http://localhost:8080/images/rare_cheesecake_slice.png"],
        details: ProductDetails(
            ingredients: "クリームチーズ（オーストラリア製造）、生クリーム、砂糖、ヨーグルト、レモン果汁、ゼラチン、グラハムクラッカー、バター／乳化剤、香料、（一部に小麦・乳成分を含む）",
            nutrition: "100gあたり：エネルギー 315kcal、タンパク質 5.2g、脂質 21.3g、炭水化物 25.7g",
            expiration: "冷凍保存で約3ヶ月（推奨）、解凍後は冷蔵で2日",
            storage: "冷凍（-18℃以下）で保存してください"
        )
    )
    
    static let newArrivals: [Product] = [
        strawberryMontBlanc,
        pistachioMousse,
        matchaTiramisu,
        rareCheesecake
    ]
    
    static let allProducts: [Product] = rankingProducts + newArrivals + [fruitCakeDetail, shortCakeDetail, setItemDetail]
    
    static let news: [NewsItem] = [
        NewsItem(date: "2026.01.21", title: "【重要】天候不良による配送への影響について"),
        NewsItem(date: "2025.07.08", title: "【重要】商品価格改定のお知らせ"),
        NewsItem(date: "2025.03.12", title: "【重要】4/1(火)より領収書の完全ペーパーレス化のお知らせ"),
        NewsItem(date: "2024.12.20", title: "年末年始の営業について")
    ]
}
