# 多智能体AI股票分析师

一个强大的多智能体系统，利用人工智能对股票进行深度分析并生成专业投资报告。

[![部署到Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2Fyourusername%2Fmulti_agent_financial_analyst)

## 🎯 核心亮点

- **股票分析智能体**：深度融合基本面与技术面指标，全方位解析股票价值
- **报告撰写智能体**：将复杂数据转化为清晰易懂的专业级投资报告
- **实时市场数据流接入** | **动态可视化分析** | **一键生成Markdown格式报告**

## 项目核心架构

项目采用了一个由两个专业AI智能体组成的系统：

1. **股票分析智能体**：负责收集和分析股票数据
2. **报告撰写智能体**：将分析转化为专业报告

两个智能体通过 CrewAI 框架进行协作，按顺序执行任务，形成一个完整的工作流程。

## 技术组成

项目主要由以下几个部分组成：

1. **核心文件**
   - `financial_analyst.py`：主程序，包含Streamlit界面和智能体配置
   - `financial_tools.py`：包含用于获取股票数据的工具

2. **主要技术栈**
   - Streamlit：用于构建Web界面
   - CrewAI：用于配置和管理多智能体工作流
   - SambaNova AI LLM：使用Llama-4-Maverick-17B大型语言模型
   - YFinance：用于获取实时股票数据

3. **数据流程**
   
   数据流向为：yfinance API → 股票分析智能体 → 报告撰写智能体 → Streamlit界面

## ⚡ 快速启动指南

### 1️⃣ 克隆仓库

```bash
git clone https://github.com/yourusername/multi_agent_financial_analyst.git
cd multi_agent_financial_analyst
```

### 2️⃣ 安装依赖

```bash
pip install -r requirements.txt
```

### 3️⃣ 配置环境密钥

在项目根目录创建`.env`文件并填入：

```
SAMBANOVA_API_KEY=你的API密钥
```

### 4️⃣ 启动应用

```bash
streamlit run financial_analyst.py
```

## 🌐 交互体验

- 运行命令启动应用
- 输入股票代码（如AAPL）
- 点击「智能分析」触发多智能体协作
- 30秒内获得含买卖建议的完整报告

## 🤖 技术内幕

### 双智能体协同作战

#### 🔍 分析引擎
- 财务健康度扫描
- 新闻情绪雷达监测
- MACD/RSI多指标融合诊断

#### ✍️ 报告大师
- 自动生成华尔街级分析框架
- 关键数据高亮标记
- 风险提示智能标注

## 📤 部署指南

### Vercel部署

1. 点击上方的"部署到Vercel"按钮
2. 登录您的Vercel账户
3. 设置环境变量`SAMBANOVA_API_KEY`
4. 完成部署流程

### 本地部署

按照上述"快速启动指南"进行本地部署。

## 注意事项

- 本项目需要SambaNova AI API密钥，请在[官方网站](https://sambanova.ai/)申请
- 分析结果仅供参考，不构成投资建议
- YFinance API可能存在数据延迟，实际交易前请核实数据 