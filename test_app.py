import streamlit as st
import os
import sys

# 显示标题
st.title("Streamlit 测试应用")

# 检查环境变量和密钥设置
st.subheader("环境配置检查")

try:
    if "deepseek_api_key" in st.secrets:
        st.success("成功：Streamlit Secrets 中找到 deepseek_api_key")
    else:
        st.warning("警告：Streamlit Secrets 中未找到 deepseek_api_key")
except:
    st.error("错误：无法访问 Streamlit Secrets")

deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")
if deepseek_api_key:
    st.success("成功：环境变量中找到 DEEPSEEK_API_KEY")
else:
    st.warning("警告：环境变量中未找到 DEEPSEEK_API_KEY")

# 显示系统信息
st.subheader("系统信息")
st.text(f"Python 版本: {sys.version}")

# 检查 SQLite 版本
st.subheader("SQLite 版本检查")

try:
    import sqlite3
    sqlite_version = sqlite3.sqlite_version
    sqlite_version_info = sqlite3.sqlite_version_info
    required_version = (3, 35, 0)
    
    st.text(f"SQLite 版本: {sqlite_version}")
    
    if sqlite_version_info < required_version:
        st.error(f"SQLite 版本 {sqlite_version} 低于 ChromaDB 要求的 3.35.0")
        st.info("解决方案: 1) 使用 pysqlite3-binary 替代库; 2) 设置环境变量绕过检查")
    else:
        st.success(f"SQLite 版本 {sqlite_version} 兼容 ChromaDB 要求")
except Exception as e:
    st.error(f"检查 SQLite 版本时出错: {str(e)}")

# 尝试导入基本依赖
st.subheader("基本依赖项检查")

basic_dependencies = [
    "streamlit", "requests", "pandas", "numpy", "matplotlib", "plotly"
]

for dep in basic_dependencies:
    try:
        module = __import__(dep)
        st.success(f"成功: {dep} 已安装，版本 {module.__version__ if hasattr(module, '__version__') else '未知'}")
    except ImportError:
        st.error(f"失败: {dep} 未安装或无法导入")
    except Exception as e:
        st.warning(f"警告: {dep} 导入时发生错误: {str(e)}")

# 尝试导入高级依赖（可能会失败，但不会阻止应用运行）
st.subheader("高级依赖项检查")

advanced_dependencies = [
    "langchain", "crewai", "langchain_community", "chromadb"
]

for dep in advanced_dependencies:
    try:
        module = __import__(dep)
        st.success(f"成功: {dep} 已安装，版本 {module.__version__ if hasattr(module, '__version__') else '未知'}")
    except ImportError:
        st.error(f"失败: {dep} 未安装或无法导入")
    except Exception as e:
        st.warning(f"警告: {dep} 导入时发生错误: {str(e)}")

# 检查环境变量
st.subheader("环境变量检查")
env_vars = [
    "CHROMA_DB_FORCE_DISABLE_VERSION_CHECK", 
    "ALLOW_SQLITE_VERSION", 
    "DEEPSEEK_API_KEY"
]

for var in env_vars:
    if os.getenv(var):
        st.info(f"环境变量 {var} 已设置为: {os.getenv(var)[:3]}..." if var == "DEEPSEEK_API_KEY" else f"环境变量 {var} 已设置为: {os.getenv(var)}")
    else:
        st.warning(f"环境变量 {var} 未设置")

# 简单的用户交互演示
st.subheader("简单交互测试")
text_input = st.text_input("输入文本", "测试文本")
st.write(f"您输入的文本: {text_input}")

if st.button("测试按钮"):
    st.info("按钮已点击！")
    
# 页脚
st.markdown("---")
st.markdown("**多智能体AI股票分析师** | 测试应用") 