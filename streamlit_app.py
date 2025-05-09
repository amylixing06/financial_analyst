# 这是 Streamlit Cloud 默认寻找的入口文件
# 直接导入 financial_analyst.py 中的全部内容

# 导入必要的库
import streamlit as st
import os
import json
from dotenv import load_dotenv

# 确保 SQLite 兼容性
try:
    from sqlite_patch import apply_sqlite_patch
    apply_sqlite_patch()
except ImportError:
    # 如果无法导入补丁，不阻止应用运行
    pass

# 导入 financial_analyst.py 中的功能
from financial_analyst import *

# 注意：由于 financial_analyst.py 中已经包含了 Streamlit 界面代码
# 导入该模块时会自动运行其中的 Streamlit 应用 

# 简化错误处理和导入
def main():
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
    st.info("应用正在初始化中，这可能需要一些时间...")

    try:
        # 导入必要的模块
        from financial_analyst import analyze_stock, setup_deepseek
        
        # 确保DeepSeek配置正确
        if not setup_deepseek():
            # 尝试直接获取 API 密钥
            api_key = None
            try:
                api_key = st.secrets["deepseek_api_key"]
            except:
                pass
                
            if api_key:
                os.environ["DEEPSEEK_API_KEY"] = api_key
                st.success("已从 Streamlit Secrets 加载 API 密钥")
            else:
                st.error("DeepSeek API 密钥配置错误")
                st.info("请在 Streamlit Cloud 的 Secrets 管理中设置 deepseek_api_key")
                st.stop()
        
        # 股票代码输入
        with st.form("stock_form"):
            ticker_symbol = st.text_input("输入股票代码 (例如: AAPL, MSFT)", placeholder="AAPL")
            col1, col2 = st.columns([1, 5])
            with col1:
                submit_button = st.form_submit_button("智能分析")
            with col2:
                st.markdown("*分析过程可能需要30-60秒，请耐心等待*")

        # 当用户提交股票代码
        if submit_button and ticker_symbol:
            with st.spinner(f"AI智能体正在分析 {ticker_symbol} 股票..."):
                report = analyze_stock(ticker_symbol)
            
            # 显示报告
            st.markdown("## 📝 AI分析报告")
            st.markdown(report)
            
            # 提供下载选项
            st.download_button(
                label="下载报告 (Markdown)",
                data=report,
                file_name=f"{ticker_symbol}_分析报告.md",
                mime="text/markdown"
            )
    except Exception as e:
        st.error(f"应用加载出错: {str(e)}")
        st.info("请检查日志以获取更多详细信息。")

    # 页脚
    st.markdown("---")
    st.markdown("**多智能体AI股票分析师** | 由DeepSeek和CrewAI提供支持")

# 当直接运行此文件时
if __name__ == "__main__":
    main() 