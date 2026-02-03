# -*- coding: utf-8 -*-
"""
MonotaRO Q&A System - Flask Backend
電商客服シミュ レーション Web アプリケーション
"""

import os
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from inference import get_inference_engine

# Flask アプリケーション
app = Flask(__name__)
CORS(app)

# 設定
app.config['JSON_AS_ASCII'] = False


@app.route('/')
def index():
    """メインページを表示"""
    return render_template('index.html')


@app.route('/api/categories', methods=['GET'])
def get_categories():
    """カテゴリ一覧を取得"""
    engine = get_inference_engine()
    categories = engine.get_categories()
    return jsonify({"categories": categories})


@app.route('/api/products/<int:category_id>', methods=['GET'])
def get_products(category_id):
    """指定カテゴリの商品一覧を取得"""
    engine = get_inference_engine()
    products = engine.get_products(category_id)
    return jsonify({"products": products, "category_id": category_id})


@app.route('/api/select_category', methods=['POST'])
def select_category():
    """カテゴリを選択"""
    try:
        data = request.get_json()
        category_id = data.get('category_id')
        
        if category_id is None:
            return jsonify({"error": "category_id が必要です"}), 400
        
        engine = get_inference_engine()
        result = engine.set_category(category_id)
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/select_product', methods=['POST'])
def select_product():
    """商品を選択"""
    try:
        data = request.get_json()
        product_name = data.get('product_name')
        
        if not product_name:
            return jsonify({"error": "product_name が必要です"}), 400
        
        engine = get_inference_engine()
        result = engine.set_product(product_name)
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/chat', methods=['POST'])
def chat():
    """チャット API"""
    try:
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({"error": "メッセージが必要です"}), 400
        
        message = data['message'].strip()
        
        if not message:
            return jsonify({"error": "空のメッセージは送信できません"}), 400
        
        if len(message) > 1000:
            return jsonify({"error": "メッセージが長すぎます"}), 400
        
        engine = get_inference_engine()
        result = engine.generate_response(message)
        
        return jsonify(result)
    
    except Exception as e:
        print(f"[Error] {str(e)}")
        return jsonify({"error": "サーバーエラーが発生しました"}), 500


@app.route('/api/reset', methods=['POST'])
def reset_dialogue():
    """対話をリセット"""
    engine = get_inference_engine()
    result = engine.reset_dialogue()
    return jsonify(result)


@app.route('/api/status', methods=['GET'])
def get_status():
    """現在の状態を取得"""
    engine = get_inference_engine()
    return jsonify({
        "current_category": engine.current_category,
        "current_product": engine.current_product,
        "model_loaded": engine.model_loaded,
        "dialogue_length": len(engine.dialogue_history),
    })


@app.route('/api/health', methods=['GET'])
def health_check():
    """ヘルスチェック"""
    engine = get_inference_engine()
    return jsonify({
        "status": "healthy",
        "service": "MonotaRO Q&A System",
        "model_loaded": engine.model_loaded,
    })


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    debug = os.environ.get('DEBUG', 'true').lower() == 'true'
    
    print("=" * 60)
    print(" MonotaRO Q&A System (E-Commerce Customer Service)")
    print("=" * 60)
    print(f" URL: http://localhost:{port}")
    print(f" Debug: {debug}")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=port, debug=debug)
