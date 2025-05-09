#!/bin/bash

# 安装依赖
pip install -r requirements.txt

# 创建配置文件
mkdir -p .streamlit
echo '[server]
headless = true
port = 8501
enableCORS = true' > .streamlit/config.toml 