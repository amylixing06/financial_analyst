import streamlit as st
import os

# 显示标题
st.title("Streamlit 测试应用")

# 检查环境变量和密钥设置
st.subheader("环境配置检查")

try:
    if "openai_api_key" in st.secrets:
        st.success("成功：Streamlit Secrets 中找到 openai_api_key")
    else:
        st.warning("警告：Streamlit Secrets 中未找到 openai_api_key")
except:
    st.error("错误：无法访问 Streamlit Secrets")

openai_api_key = os.getenv("OPENAI_API_KEY")
if openai_api_key:
    st.success("成功：环境变量中找到 OPENAI_API_KEY")
else:
    st.warning("警告：环境变量中未找到 OPENAI_API_KEY")

# 显示系统信息
st.subheader("系统信息")
st.text(f"Python 版本: {os.sys.version}")

# 尝试导入基本依赖
st.subheader("基本依赖项检查")

basic_dependencies = [
    "streamlit", "openai", "pandas", "numpy", "matplotlib", "plotly"
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
    "langchain", "crewai", "langchain_community", 
]

for dep in advanced_dependencies:
    try:
        module = __import__(dep)
        st.success(f"成功: {dep} 已安装，版本 {module.__version__ if hasattr(module, '__version__') else '未知'}")
    except ImportError:
        st.error(f"失败: {dep} 未安装或无法导入")
    except Exception as e:
        st.warning(f"警告: {dep} 导入时发生错误: {str(e)}")

# 简单的用户交互演示
st.subheader("简单交互测试")
text_input = st.text_input("输入文本", "测试文本")
st.write(f"您输入的文本: {text_input}")

if st.button("测试按钮"):
    st.info("按钮已点击！")
    
# 页脚
st.markdown("---")
st.markdown("**多智能体AI股票分析师** | 测试应用") 