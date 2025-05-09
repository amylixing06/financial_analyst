# 多智能体AI股票分析师

一个由DeepSeek驱动的AI股票分析系统，利用多智能体架构进行全面的股票分析和报告生成。

## 功能特点

- 股票基本面和技术面全面分析
- 多智能体协作（分析师智能体 + 报告撰写智能体）
- 生成专业格式的Markdown投资报告
- 使用DeepSeek AI模型提供强大的推理和分析能力

## 安装与设置

1. 克隆仓库并安装依赖：

```bash
git clone https://github.com/yourusername/financial_analyst.git
cd financial_analyst
pip install -r requirements.txt
```

2. 获取DeepSeek API密钥:

   - 访问 [DeepSeek开发者平台](https://platform.deepseek.com)
   - 注册并创建API密钥
   - 复制API密钥

3. 设置环境变量：

   - 将`sample.env`复制为`.env`
   - 编辑`.env`文件，添加您的DeepSeek API密钥:
   ```
   DEEPSEEK_API_KEY=您的DeepSeek_API密钥
   ```

## 使用方法

### 本地运行

```bash
streamlit run streamlit_app.py
```

### Streamlit Cloud部署

1. 在Streamlit Cloud中，设置以下Secrets:
   - `deepseek_api_key`: 您的DeepSeek API密钥

2. 指向`streamlit_app.py`作为主要入口点

## 代码结构

- `streamlit_app.py`: 主应用入口点
- `financial_analyst.py`: 主要业务逻辑和智能体定义
- `financial_tools.py`: 用于股票分析的工具集合
- `deepseek_api.py`: DeepSeek API封装模块
- `bootstrap.py`: 应用引导脚本，处理环境兼容性
- `sqlite_patch.py`: SQLite版本兼容补丁
- `simple_app.py`: 简化版应用（用于调试）
- `test_app.py`: 测试工具（用于验证环境）

## 为什么使用DeepSeek

DeepSeek提供了强大的语言理解和分析能力，特别是在复杂推理任务方面表现优异。我们使用:

- DeepSeek-V3(`deepseek-chat`)：用于一般对话和报告生成
- DeepSeek-R1(`deepseek-reasoner`)：用于复杂分析和推理任务

## 技术栈

- Streamlit：用户界面
- DeepSeek API：大型语言模型
- yfinance：股票数据获取
- pandas/numpy：数据处理
- langchain：大型语言模型框架
- plotly：数据可视化

## 常见问题

**Q: 我在Streamlit Cloud上部署时遇到问题？**

A: 确保在Streamlit Cloud Secrets中设置了`deepseek_api_key`。此外，应用使用渐进式加载策略，如果遇到问题，会自动降级到简化版本。

**Q: 分析需要多长时间？**

A: 通常需要30-60秒完成一次完整分析。这取决于模型的负载和要分析的股票复杂度。

**Q: 我需要付费吗？**

A: 您需要有自己的DeepSeek API账户和密钥。DeepSeek提供一定数量的免费额度，但超出后需要付费。

## 贡献

欢迎提交问题和拉取请求！如果您有改进建议，请随时与我们联系。

## 许可证

MIT 