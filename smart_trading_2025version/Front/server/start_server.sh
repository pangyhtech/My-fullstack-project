#!/bin/bash
# 安装依赖
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
 
# 启动服务器
echo "正在启动OKCoin交易API服务器..."
python app.py 