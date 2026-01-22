#!/usr/bin/env python3
"""
Simple HTTP server for serving product images and data
"""
from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
import os

import os
import uuid
from datetime import datetime, timedelta

# In-memory storage (in production, use a database)
users_db = {}
favorites_db = {}  # user_id -> set of product_ids
reviews_db = {}    # product_id -> list of reviews
orders_db = {}     # order_id -> order data
coupons_db = {}    # coupon_id -> coupon data

# Initialize mock coupons
def init_mock_coupons():
    future_date = (datetime.now() + timedelta(days=30)).isoformat()
    coupons_db['coupon_1'] = {
        'id': 'coupon_1',
        'code': 'WELCOME10',
        'title': '新規会員限定10%OFF',
        'discountType': 'percentage',
        'discountValue': 10,
        'minPurchase': 3000,
        'expiryDate': future_date,
        'isUsed': False,
        'createdAt': datetime.now().isoformat()
    }
    coupons_db['coupon_2'] = {
        'id': 'coupon_2',
        'code': 'SAVE500',
        'title': '500円OFFクーポン',
        'discountType': 'fixed',
        'discountValue': 500,
        'minPurchase': 5000,
        'expiryDate': future_date,
        'isUsed': False,
        'createdAt': datetime.now().isoformat()
    }

init_mock_coupons()

class CORSRequestHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, OPTIONS, DELETE')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()
    
    def do_PUT(self):
        content_length = int(self.headers.get('Content-Length', 0))
        put_data = self.rfile.read(content_length).decode('utf-8')
        
        if self.path.startswith('/api/users/'):
            user_id = self.path.split('/')[-1]
            self.handle_update_user(user_id, put_data)
        else:
            self.send_error(404)
    
    def handle_update_user(self, user_id, data):
        try:
            if user_id not in users_db:
                self.send_error(404, 'User not found')
                return
            
            update_data = json.loads(data)
            # Update allowed fields
            for field in ['name', 'email', 'phoneNumber', 'postalCode', 'address']:
                if field in update_data:
                    users_db[user_id][field] = update_data[field]
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(users_db[user_id], ensure_ascii=False).encode('utf-8'))
        except Exception as e:
            self.send_error(400, str(e))
    
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length).decode('utf-8')
        
        if self.path == '/api/users':
            self.handle_create_user(post_data)
        elif self.path.startswith('/api/favorites'):
            self.handle_favorite_toggle(post_data)
        elif self.path == '/api/reviews':
            self.handle_create_review(post_data)
        elif self.path == '/api/orders':
            self.handle_create_order(post_data)
        elif self.path == '/api/coupons':
            self.handle_create_coupon(post_data)
        elif self.path.startswith('/api/coupons/use'):
            self.handle_use_coupon(post_data)
        else:
            self.send_error(404)
    
    def do_DELETE(self):
        if self.path.startswith('/api/users/'):
            user_id = self.path.split('/')[-1]
            self.handle_delete_user(user_id)
        elif self.path.startswith('/api/coupons/'):
            coupon_id = self.path.split('/')[-1]
            self.handle_delete_coupon(coupon_id)
        else:
            self.send_error(404)
    
    def handle_delete_user(self, user_id):
        try:
            if user_id in users_db:
                del users_db[user_id]
                if user_id in favorites_db:
                    del favorites_db[user_id]
                # Also delete user's orders
                orders_to_delete = [oid for oid, order in orders_db.items() if order.get('userId') == user_id]
                for oid in orders_to_delete:
                    del orders_db[oid]
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'success': True, 'message': 'Account deleted'}).encode('utf-8'))
            else:
                self.send_error(404, 'User not found')
        except Exception as e:
            self.send_error(400, str(e))
    
    def handle_delete_coupon(self, coupon_id):
        try:
            if coupon_id in coupons_db:
                del coupons_db[coupon_id]
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'success': True}).encode('utf-8'))
            else:
                self.send_error(404, 'Coupon not found')
        except Exception as e:
            self.send_error(400, str(e))
    
    def handle_create_user(self, data):
        try:
            user_data = json.loads(data)
            user_id = str(uuid.uuid4())
            users_db[user_id] = {
                'id': user_id,
                'name': user_data.get('name'),
                'email': user_data.get('email'),
                'phoneNumber': user_data.get('phoneNumber', ''),
                'postalCode': user_data.get('postalCode', ''),
                'address': user_data.get('address', ''),
                'created_at': datetime.now().isoformat()
            }
            favorites_db[user_id] = set()
            
            self.send_response(201)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(users_db[user_id], ensure_ascii=False).encode('utf-8'))
        except Exception as e:
            self.send_error(400, str(e))
    
    def handle_favorite_toggle(self, data):
        try:
            fav_data = json.loads(data)
            user_id = fav_data.get('user_id')
            product_id = fav_data.get('product_id')
            
            if user_id not in favorites_db:
                favorites_db[user_id] = set()
            
            if product_id in favorites_db[user_id]:
                favorites_db[user_id].remove(product_id)
                action = 'removed'
            else:
                favorites_db[user_id].add(product_id)
                action = 'added'
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                'action': action,
                'favorites': list(favorites_db[user_id])
            }
            self.wfile.write(json.dumps(response).encode('utf-8'))
        except Exception as e:
            self.send_error(400, str(e))
    
    def handle_create_review(self, data):
        try:
            review_data = json.loads(data)
            product_id = review_data.get('product_id')
            
            if product_id not in reviews_db:
                reviews_db[product_id] = []
            
            review = {
                'id': str(uuid.uuid4()),
                'product_id': product_id,
                'user_id': review_data.get('user_id'),
                'user_name': review_data.get('user_name'),
                'rating': review_data.get('rating'),
                'comment': review_data.get('comment'),
                'date': datetime.now().isoformat()
            }
            reviews_db[product_id].insert(0, review)
            
            self.send_response(201)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(review, ensure_ascii=False).encode('utf-8'))
        except Exception as e:
            self.send_error(400, str(e))
    
    def handle_create_order(self, data):
        try:
            order_data = json.loads(data)
            order_id = str(uuid.uuid4())
            order = {
                'id': order_id,
                'userId': order_data.get('userId'),
                'items': order_data.get('items', []),
                'totalAmount': order_data.get('totalAmount'),
                'deliveryFee': order_data.get('deliveryFee'),
                'deliveryDate': order_data.get('deliveryDate'),
                'deliveryTime': order_data.get('deliveryTime'),
                'paymentMethod': order_data.get('paymentMethod'),
                'status': 'pending',
                'createdAt': datetime.now().isoformat()
            }
            orders_db[order_id] = order
            
            self.send_response(201)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(order, ensure_ascii=False).encode('utf-8'))
        except Exception as e:
            self.send_error(400, str(e))
    
    def handle_create_coupon(self, data):
        try:
            coupon_data = json.loads(data)
            coupon_id = str(uuid.uuid4())
            coupon = {
                'id': coupon_id,
                'code': coupon_data.get('code'),
                'title': coupon_data.get('title'),
                'discountType': coupon_data.get('discountType'),
                'discountValue': coupon_data.get('discountValue'),
                'minPurchase': coupon_data.get('minPurchase', 0),
                'expiryDate': coupon_data.get('expiryDate'),
                'isUsed': False,
                'createdAt': datetime.now().isoformat()
            }
            coupons_db[coupon_id] = coupon
            
            self.send_response(201)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(coupon, ensure_ascii=False).encode('utf-8'))
        except Exception as e:
            self.send_error(400, str(e))
    
    def handle_use_coupon(self, data):
        try:
            use_data = json.loads(data)
            coupon_id = use_data.get('couponId')
            
            if coupon_id in coupons_db:
                coupons_db[coupon_id]['isUsed'] = True
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(coupons_db[coupon_id], ensure_ascii=False).encode('utf-8'))
            else:
                self.send_error(404, 'Coupon not found')
        except Exception as e:
            self.send_error(400, str(e))
    
    
    def do_GET(self):
        if self.path == '/api/products':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            products = self.get_products_data()
            self.wfile.write(json.dumps(products, ensure_ascii=False).encode('utf-8'))
        elif self.path.startswith('/api/users/'):
            user_id = self.path.split('/')[-1]
            self.handle_get_user(user_id)
        elif self.path.startswith('/api/favorites/'):
            user_id = self.path.split('/')[-1]
            self.handle_get_favorites(user_id)
        elif self.path.startswith('/api/reviews/'):
            product_id = self.path.split('/')[-1]
            self.handle_get_reviews(product_id)
        elif self.path == '/api/users':
            self.handle_get_all_users()
        elif self.path == '/api/orders':
            self.handle_get_all_orders()
        elif self.path.startswith('/api/orders/user/'):
            user_id = self.path.split('/')[-1]
            self.handle_get_user_orders(user_id)
        elif self.path == '/api/coupons':
            self.handle_get_all_coupons()
        else:
            super().do_GET()
    
    def handle_get_user(self, user_id):
        if user_id in users_db:
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(users_db[user_id], ensure_ascii=False).encode('utf-8'))
        else:
            self.send_error(404, 'User not found')
    
    def handle_get_favorites(self, user_id):
        if user_id in favorites_db:
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(list(favorites_db[user_id])).encode('utf-8'))
        else:
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps([]).encode('utf-8'))
    
    def handle_get_reviews(self, product_id):
        reviews = reviews_db.get(product_id, [])
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(reviews, ensure_ascii=False).encode('utf-8'))
    
    def handle_get_all_users(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(list(users_db.values()), ensure_ascii=False).encode('utf-8'))
    
    def handle_get_all_orders(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(list(orders_db.values()), ensure_ascii=False).encode('utf-8'))
    
    def handle_get_user_orders(self, user_id):
        user_orders = [order for order in orders_db.values() if order.get('userId') == user_id]
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(user_orders, ensure_ascii=False).encode('utf-8'))
    
    def handle_get_all_coupons(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(list(coupons_db.values()), ensure_ascii=False).encode('utf-8'))
    
    def get_products_data(self):
        base_url = "http://localhost:8080/images"
        return {
            "products": [
                {
                    "id": "strawberry_montblanc",
                    "name": "あまおう苺のモンブラン (4個入)",
                    "price": 1480,
                    "imageUrl": f"{base_url}/strawberry_montblanc_cake.png",
                    "badge": "NEW",
                    "category": "モンブラン"
                },
                {
                    "id": "pistachio_mousse",
                    "name": "ピスタチオムース",
                    "price": 1550,
                    "imageUrl": f"{base_url}/pistachio_mousse_cake.png",
                    "badge": "NEW",
                    "category": "ムースケーキ"
                },
                {
                    "id": "matcha_tiramisu",
                    "name": "宇治抹茶ティラミス",
                    "price": 1620,
                    "imageUrl": f"{base_url}/matcha_tiramisu_dessert.png",
                    "badge": "Limited",
                    "category": "ティラミス"
                },
                {
                    "id": "rare_cheesecake",
                    "name": "レアチーズケーキ 5号",
                    "price": 2800,
                    "imageUrl": f"{base_url}/rare_cheesecake_slice.png",
                    "category": "チーズケーキ"
                },
                {
                    "id": "fruit_tart",
                    "name": "彩りフルーツのタルト 5号",
                    "price": 3200,
                    "imageUrl": f"{base_url}/fruit_tart_cake.png",
                    "badge": "Seasonal",
                    "category": "フルーツケーキ"
                },
                {
                    "id": "hokkaido_shortcake",
                    "name": "北海道生クリームのショートケーキ",
                    "price": 3800,
                    "imageUrl": f"{base_url}/hokkaido_shortcake.png",
                    "category": "ショートケーキ"
                },
                {
                    "id": "cake_set",
                    "name": "人気ケーキ3種食べ比べセット",
                    "price": 2980,
                    "imageUrl": f"{base_url}/cake_assortment_set.png",
                    "badge": "Gift",
                    "category": "セット商品"
                }
            ]
        }

if __name__ == '__main__':
    PORT = 8080
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    print(f"Starting server on http://localhost:{PORT}")
    print("Product API available at http://localhost:8080/api/products")
    print("Images available at http://localhost:8080/images/")
    print("Press Ctrl+C to stop")
    
    httpd = HTTPServer(('localhost', PORT), CORSRequestHandler)
    httpd.serve_forever()
