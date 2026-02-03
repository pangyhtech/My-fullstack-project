# SweetsPro バックエンドサーバー

[English](README.md) | [日本語](README_JP.md)

---

## クイックスタート
```bash
cd sweetspro_v1.0.0/server
python3 server.py
```

サーバー起動: **http://localhost:8080**

## APIエンドポイント
- 商品: `GET /api/products`
- 画像: `GET /images/{image_name}.png`

## 技術
- Python 3.x
- HTTPServer
- インメモリストレージ

## iOS統合
**シミュレーター:** `localhost:8080`を使用  
**実機:** MacのIPアドレスに置き換え
