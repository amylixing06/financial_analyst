# 在Heroku上部署AI股票分析应用

本指南将帮助您使用提供的脚本将AI股票分析应用部署到Heroku平台。

## 准备工作

1. 确保您有一个Heroku账户。如果没有，请前往[Heroku官网](https://www.heroku.com/)注册。
2. 确保您的机器上已安装Git（部署脚本会检查并尝试安装Heroku CLI）。

## 部署步骤

1. 打开终端，进入项目根目录：
   ```bash
   cd path/to/financial_analyst
   ```

2. 确保部署脚本有执行权限：
   ```bash
   chmod +x deploy_to_heroku.sh
   ```

3. 运行部署脚本：
   ```bash
   ./deploy_to_heroku.sh
   ```

4. 按照提示操作：
   - 如果未安装Heroku CLI，脚本会尝试安装
   - 需要登录Heroku账户
   - 需要输入您的DeepSeek API密钥

5. 部署完成后，脚本会自动打开浏览器访问您的应用。

## 部署细节

脚本会自动完成以下操作：

- 检查并安装Heroku CLI
- 登录Heroku账户
- 创建必要的Heroku配置文件（Procfile和runtime.txt）
- 创建一个新的Heroku应用
- 配置环境变量（DeepSeek API密钥）
- 将代码推送到Heroku
- 启动应用

## 常见问题

### 应用崩溃或无法启动

1. 检查日志以获取错误信息：
   ```bash
   heroku logs --tail -a your-app-name
   ```

2. 确保API密钥正确配置：
   ```bash
   heroku config -a your-app-name
   ```

### 应用经常休眠

Heroku免费套餐的应用在30分钟不活动后会休眠。解决方法：

1. 升级到付费套餐
2. 使用第三方服务定期ping您的应用，如[Kaffeine](https://kaffeine.herokuapp.com/)

### 如何更新已部署的应用

1. 提交您的更改到Git
2. 推送到Heroku：
   ```bash
   git push heroku main
   ```

## 注意事项

- Heroku免费套餐有550小时/月的限制（添加信用卡后为1000小时/月）
- 应用没有永久存储，重启后数据会丢失
- 如需持久化存储，请考虑添加Heroku附加组件如Postgres 