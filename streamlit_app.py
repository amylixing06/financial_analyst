# 这是 Streamlit Cloud 默认寻找的入口文件
# 使用bootstrap.py作为实际入口点，它会自动处理兼容性问题

import streamlit as st
import os
import sys

# 显示欢迎页面
st.set_page_config(
    page_title="多智能体AI股票分析师",
    page_icon="📊",
    layout="wide"
)

st.title("🤖 多智能体AI股票分析师")
st.markdown("""
### 由双智能体驱动的专业股票分析系统
本系统由股票分析智能体和报告撰写智能体协作完成分析，提供全面、专业的股票投资报告。
""")

# 显示加载状态
st.info("正在加载引导程序，请稍候...")

# 尝试导入引导模块
try:
    import bootstrap
    # bootstrap.py会自动检测环境并加载适当的应用版本
except Exception as e:
    st.error(f"引导程序加载失败: {str(e)}")
    st.info("正在尝试加载简化版应用...")
    
    try:
        import simple_app
    except Exception as e:
        st.error(f"应用加载失败: {str(e)}")
        st.info("请检查环境配置或联系支持团队。") 