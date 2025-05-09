#!/bin/bash
# 部署股票分析应用到阿里云服务器
# 使用方法: 将此脚本上传到服务器后运行

# 输出颜色设置
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}开始部署股票分析应用到阿里云服务器...${NC}"

# 确认是否是root用户运行
if [ "$EUID" -ne 0 ]
  then echo -e "${RED}请使用root用户运行此脚本（sudo ./deploy_to_aliyun.sh）${NC}"
  exit
fi

# 更新系统包
echo -e "${BLUE}更新系统包...${NC}"
apt update
apt upgrade -y

# 安装必要的软件
echo -e "${BLUE}安装必要的软件...${NC}"
apt install -y python3 python3-pip python3-venv nginx git supervisor

# 创建应用目录
echo -e "${BLUE}创建应用目录...${NC}"
mkdir -p /opt/financial_analyst
cd /opt/financial_analyst

# 克隆代码仓库或解压上传的文件
if [ -d ".git" ]; then
    echo -e "${BLUE}代码仓库已存在，更新代码...${NC}"
    git pull
else
    echo -e "${BLUE}克隆代码仓库...${NC}"
    # 替换为您的实际代码仓库URL
    git clone https://github.com/yourusername/financial_analyst.git .
fi

# 创建虚拟环境
echo -e "${BLUE}创建Python虚拟环境...${NC}"
python3 -m venv venv
source venv/bin/activate

# 安装依赖
echo -e "${BLUE}安装Python依赖...${NC}"
pip install --upgrade pip
pip install -r requirements.txt

# 创建环境变量文件
echo -e "${BLUE}配置环境变量...${NC}"
cat > .env << EOL
# DeepSeek API密钥
DEEPSEEK_API_KEY=您的DeepSeek_API密钥
EOL

echo -e "${GREEN}请编辑 /opt/financial_analyst/.env 文件，填入您的API密钥${NC}"

# 创建Streamlit配置目录
mkdir -p /root/.streamlit
cat > /root/.streamlit/config.toml << EOL
[server]
headless = true
port = 8501
enableCORS = false
enableXsrfProtection = true
EOL

# 创建Supervisor配置
echo -e "${BLUE}配置Supervisor...${NC}"
cat > /etc/supervisor/conf.d/financial_analyst.conf << EOL
[program:financial_analyst]
command=/opt/financial_analyst/venv/bin/streamlit run /opt/financial_analyst/streamlit_app.py
directory=/opt/financial_analyst
user=root
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true
environment=PYTHONPATH="/opt/financial_analyst",HOME="/root"
stderr_logfile=/var/log/financial_analyst/stderr.log
stdout_logfile=/var/log/financial_analyst/stdout.log
EOL

# 创建日志目录
mkdir -p /var/log/financial_analyst

# 配置Nginx
echo -e "${BLUE}配置Nginx...${NC}"
cat > /etc/nginx/sites-available/financial_analyst << EOL
server {
    listen 80;
    server_name _;  # 替换为您的域名

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host \$host;
        proxy_cache_bypass \$http_upgrade;
        proxy_buffering off;
    }
}
EOL

# 启用Nginx配置
ln -sf /etc/nginx/sites-available/financial_analyst /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default

# 重启服务
echo -e "${BLUE}重启服务...${NC}"
systemctl restart supervisor
supervisorctl reload
systemctl restart nginx

echo -e "${GREEN}部署完成!${NC}"
echo -e "${GREEN}请访问 http://服务器IP 查看应用${NC}"
echo -e "${BLUE}如需配置自定义域名，请编辑 /etc/nginx/sites-available/financial_analyst 文件${NC}"
echo -e "${BLUE}应用日志位于 /var/log/financial_analyst/${NC}" 