# SweetsPro Backend Server

[English](#english) | [日本語](#japanese)

---

<a name="english"></a>
## English

### Quick Start
```bash
cd sweetspro_v1.0.0/server
python3 server.py
```

Server runs at: **http://localhost:8080**

### API Endpoints
- Products: `GET /api/products`
- Images: `GET /images/{image_name}.png`

### Tech
- Python 3.x
- HTTPServer
- In-memory storage

### iOS Integration
**Simulator:** Use `localhost:8080`  
**Physical Device:** Replace with Mac's IP address

---

<a name="japanese"></a>
## 日本語

### クイックスタート
```bash
cd sweetspro_v1.0.0/server
python3 server.py
```

サーバー起動: **http://localhost:8080**

### APIエンドポイント
- 商品: `GET /api/products`
- 画像: `GET /images/{image_name}.png`

### 技術
- Python 3.x
- HTTPServer
- インメモリストレージ

### iOS統合
**シミュレーター:** `localhost:8080`を使用  
**実機:** MacのIPアドレスに置き換え
