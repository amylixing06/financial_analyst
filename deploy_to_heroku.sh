#!/bin/bash
# 部署股票分析应用到Heroku
# 使用方法: ./deploy_to_heroku.sh

# 输出颜色设置
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}开始部署股票分析应用到Heroku...${NC}"

# 检查是否安装了Heroku CLI
if ! command -v heroku &> /dev/null; then
    echo -e "${RED}未安装Heroku CLI. 正在安装...${NC}"
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        brew tap heroku/brew && brew install heroku
    else
        # Linux (Ubuntu/Debian)
        curl https://cli-assets.heroku.com/install.sh | sh
    fi
    
    if ! command -v heroku &> /dev/null; then
        echo -e "${RED}Heroku CLI 安装失败. 请手动安装: https://devcenter.heroku.com/articles/heroku-cli${NC}"
        exit 1
    fi
fi

# 检查是否已登录Heroku
heroku whoami &> /dev/null
if [ $? -ne 0 ]; then
    echo -e "${BLUE}请登录Heroku...${NC}"
    heroku login
fi

# 确认当前目录是项目根目录
if [ ! -f "requirements.txt" ] || [ ! -f "streamlit_app.py" ]; then
    echo -e "${RED}当前目录可能不是项目根目录。请确保在项目根目录运行此脚本。${NC}"
    exit 1
fi

# 创建或确认Procfile
if [ ! -f "Procfile" ]; then
    echo -e "${BLUE}创建Procfile...${NC}"
    echo "web: streamlit run streamlit_app.py --server.port=\$PORT --server.headless=true" > Procfile
    echo -e "${GREEN}已创建Procfile${NC}"
else
    echo -e "${GREEN}已存在Procfile${NC}"
fi

# 确保runtime.txt已更新
echo -e "${BLUE}更新runtime.txt...${NC}"
echo "python-3.9.16" > runtime.txt

# 创建应用名称
APP_NAME="financial-analyst-$(date +%s | md5sum | head -c 6)"
echo -e "${BLUE}创建Heroku应用: $APP_NAME...${NC}"
heroku create $APP_NAME

# 配置DeepSeek API密钥
echo -e "${BLUE}配置DeepSeek API密钥...${NC}"
read -p "请输入您的DeepSeek API密钥: " API_KEY
heroku config:set DEEPSEEK_API_KEY=$API_KEY -a $APP_NAME

# 将代码推送到Heroku
echo -e "${BLUE}将代码推送到Heroku...${NC}"

# 检查是否初始化了Git
if [ ! -d ".git" ]; then
    echo -e "${BLUE}初始化Git仓库...${NC}"
    git init
    git add .
    git commit -m "初始化项目用于Heroku部署"
else
    # 检查是否有未提交的更改
    if ! git diff-index --quiet HEAD --; then
        echo -e "${BLUE}提交更改...${NC}"
        git add .
        git commit -m "准备Heroku部署"
    fi
fi

# 添加Heroku远程仓库
git remote add heroku https://git.heroku.com/$APP_NAME.git || git remote set-url heroku https://git.heroku.com/$APP_NAME.git
git push heroku master || git push heroku main

# 检查部署状态
echo -e "${BLUE}检查应用部署状态...${NC}"
heroku ps -a $APP_NAME

# 打开应用
echo -e "${GREEN}部署完成! 正在打开应用...${NC}"
heroku open -a $APP_NAME

echo -e "${GREEN}您的应用已部署到: https://$APP_NAME.herokuapp.com${NC}"
echo -e "${BLUE}查看日志: heroku logs --tail -a $APP_NAME${NC}"
echo -e "${BLUE}为确保应用保持活跃，请考虑设置以下内容:${NC}"
echo -e "${BLUE}1. 添加信用卡信息以获得更多的免费时长${NC}"
echo -e "${BLUE}2. 使用 New Relic 或 Kaffeine 等服务防止应用休眠${NC}" 