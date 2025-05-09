#!/bin/bash

# 颜色定义
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # 无颜色

echo -e "${BLUE}=== 初始化Git仓库并准备发布到GitHub ===${NC}"

# 确保在正确的目录
if [ ! -f "financial_analyst.py" ]; then
    echo "错误：请在项目根目录中运行此脚本"
    exit 1
fi

# 询问GitHub用户名
read -p "请输入您的GitHub用户名: " github_username

# 询问仓库名称
read -p "请输入您想要创建的GitHub仓库名称 (默认: multi-agent-financial-analyst): " repo_name
repo_name=${repo_name:-multi-agent-financial-analyst}

# 初始化Git仓库
echo -e "\n${GREEN}初始化Git仓库...${NC}"
git init

# 添加所有文件
echo -e "\n${GREEN}添加文件到Git...${NC}"
git add .

# 提交更改
echo -e "\n${GREEN}提交初始代码...${NC}"
git commit -m "初始提交：多智能体AI股票分析师"

# 更新README中的仓库URL
echo -e "\n${GREEN}更新README中的仓库URL...${NC}"
sed -i '' "s|https://github.com/yourusername/multi_agent_financial_analyst.git|https://github.com/$github_username/$repo_name.git|g" README.md

# 再次提交README更改
git add README.md
git commit -m "更新README中的仓库URL"

# 设置远程仓库
echo -e "\n${GREEN}设置GitHub远程仓库...${NC}"
git branch -M main
git remote add origin https://github.com/$github_username/$repo_name.git

echo -e "\n${BLUE}=== 准备工作已完成 ===${NC}"
echo -e "现在，您需要在GitHub上创建一个名为 ${repo_name} 的新仓库"
echo -e "创建后，您可以运行以下命令将代码推送到GitHub:"
echo -e "\n${GREEN}git push -u origin main${NC}"
echo -e "\n祝您项目成功！" 