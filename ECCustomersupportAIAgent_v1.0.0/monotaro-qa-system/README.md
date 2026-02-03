# MonotaRO 日本語 Q&A システム

日本語での質問に対して、AIが自動応答する Web アプリケーションです。

## 機能

- 🇯🇵 日本語の自然な対話
- 🤖 XLM-RoBERTa ベースの AI 応答
- 💬 リアルタイムチャット UI
- 📱 レスポンシブデザイン

## セットアップ

```bash
# 依存関係インストール
pip install -r requirements.txt

# サーバー起動
python app.py
```

## 使用方法

1. ブラウザで http://localhost:5000 を開く
2. 日本語で質問を入力
3. AI からの応答を確認

## API

### POST /api/chat

日本語のメッセージを送信し、AI 応答を取得します。

**リクエスト:**
```json
{
  "message": "このヘルメットいくらですか？"
}
```

**レスポンス:**
```json
{
  "response": "価格は3,280円（税込）です。",
  "confidence": 0.92,
  "category": "安全保護具"
}
```

## 技術スタック

- **Backend**: Flask + PyTorch + Transformers
- **Frontend**: HTML/CSS/JavaScript
- **Model**: XLM-RoBERTa-base
