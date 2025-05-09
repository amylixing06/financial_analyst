# AI股票分析师项目编码规范

本文档定义了AI股票分析师项目的编码规范和最佳实践。所有贡献者应遵循这些规范以保持代码的一致性和可维护性。

## 1. Python代码风格

### 1.1 基本格式
- 使用4个空格进行缩进，不使用制表符
- 每行代码不超过100个字符
- 使用双引号作为字符串的首选引号类型
- 文件末尾应有一个空行
- 删除尾随空格

### 1.2 命名规范
- 变量和函数名：使用小写字母和下划线（snake_case）
- 类名：使用首字母大写的驼峰式（PascalCase）
- 常量：使用全大写字母和下划线（UPPER_CASE）
- 模块名：使用小写字母，必要时可使用下划线

示例：
```python
GLOBAL_CONSTANT = 100

class StockAnalyzer:
    def analyze_stock_data(self, ticker_symbol):
        daily_changes = self._calculate_changes()
        return daily_changes
```

### 1.3 导入规则
- 导入应按以下顺序分组：标准库、第三方库、本地应用导入
- 每组之间应有一个空行
- 每组内按字母顺序排列

示例：
```python
# 标准库
import json
import os
from datetime import datetime

# 第三方库
import pandas as pd
import streamlit as st
import yfinance as yf

# 本地应用导入
from deepseek_api import DeepSeekAPI
from financial_tools import calculate_metrics
```

## 2. Streamlit应用规范

### 2.1 页面结构
- 使用`st.title`和`st.markdown`定义标题和主要内容
- 使用`st.container`和`st.expander`组织页面区域
- 使用`st.sidebar`放置控制元素和选项

### 2.2 用户界面
- 使用`st.spinner`显示长时间操作的加载状态
- 使用`st.form`收集用户输入，避免频繁重新运行
- 使用`st.cache_data`或`st.cache_resource`缓存长时间运行的操作

### 2.3 文本内容
- 使用Markdown格式化文本内容
- 为重要信息使用emoji增强可读性（📊 📈 🤖 等）
- 使用中文作为主要显示语言

## 3. API调用规范

### 3.1 DeepSeek API使用
- 优先使用`deepseek-reasoner`模型进行分析任务
- 设置默认温度为0.7
- 默认最大令牌数为4000
- 使用明确的系统提示设置角色和任务要求

### 3.2 错误处理
- 所有API调用应包含在try-except块中
- 捕获异常时提供友好的错误信息
- 记录详细错误日志供调试

## 4. 项目结构

### 4.1 文件组织
- 主入口文件：`streamlit_app.py`
- API接口代码：`deepseek_api.py`
- 核心功能：`financial_analyst.py`
- 简化版应用：`simple_analyst.py`
- 部署脚本：`deploy_to_heroku.sh`

### 4.2 版本控制
- 提交消息遵循格式：`类型(范围): 描述`
- 类型包括：feat, fix, docs, style, refactor, test, chore
- 保持较小的提交粒度，每个提交专注于单一职责

## 5. 文档要求

### 5.1 代码文档
- 所有函数和类应有文档字符串
- 文档字符串应包括功能描述、参数说明和返回值说明
- 复杂逻辑应有行内注释解释

### 5.2 项目文档
- README.md：项目概述、安装和使用说明
- HEROKU_DEPLOY.md：Heroku部署指南
- 其他特定文档应放在docs/目录下

## 6. 兼容性和依赖管理

### 6.1 Python版本
- 兼容Python 3.9及以上版本
- 在Heroku上使用Python 3.9.16

### 6.2 依赖管理
- 使用requirements.txt管理依赖
- 指定依赖的版本范围，避免自动升级到不兼容版本
- 避免不必要的依赖，保持简洁 