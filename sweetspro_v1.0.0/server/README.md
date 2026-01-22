# Sweets Pro 图片服务器

## 启动服务器

在终端中运行：

```bash
cd /Users/pyh0403/Desktop/sweetspro/server
python3 server.py
```

服务器将在 http://localhost:8080 启动

## 访问图片

图片URL格式：
- http://localhost:8080/images/strawberry_montblanc_cake.png
- http://localhost:8080/images/pistachio_mousse_cake.png
- http://localhost:8080/images/matcha_tiramisu_dessert.png
- http://localhost:8080/images/rare_cheesecake_slice.png
- http://localhost:8080/images/fruit_tart_cake.png
- http://localhost:8080/images/hokkaido_shortcake.png
- http://localhost:8080/images/cake_assortment_set.png

## 商品API

获取所有商品数据：
```
GET http://localhost:8080/api/products
```

## 注意事项

1. 运行iOS应用前，请确保服务器已启动
2. iOS模拟器可以访问localhost
3. 真机测试需要将localhost改为Mac的局域网IP地址
