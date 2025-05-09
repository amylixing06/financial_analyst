import streamlit as st
import os
import json
from dotenv import load_dotenv
from crewai import Agent, Task, Crew
from crewai.process import Process
from openai import OpenAI
from financial_tools import get_stock_tools

# 加载环境变量
load_dotenv()

# 配置OpenAI
def setup_openai():
    # 尝试从 Streamlit Secrets 获取 API 密钥
    try:
        api_key = st.secrets["openai_api_key"]
    except:
        # 从环境变量获取
        api_key = os.getenv("OPENAI_API_KEY")

    if api_key:
        # 初始化OpenAI客户端
        client = OpenAI(api_key=api_key)
        os.environ["OPENAI_API_KEY"] = api_key
        return True
    else:
        st.error("未找到OpenAI API密钥。请在Streamlit Cloud中设置Secrets或在本地设置环境变量。")
        return False

# 定义分析师智能体
def create_stock_analyst_agent():
    return Agent(
        role="股票分析师",
        goal="对股票进行全面分析，综合基本面和技术面因素",
        backstory="""你是一位经验丰富的股票分析师，曾在多家投行工作，擅长分析公司财务状况、
        行业趋势和技术指标。你综合多种因素做出准确的投资建议，并以客观中立的态度提供分析。""",
        verbose=True,
        allow_delegation=False,
        tools=get_stock_tools()
    )

# 定义报告编写智能体
def create_report_writer_agent():
    return Agent(
        role="投资报告撰写专家",
        goal="将复杂的股票分析结果转化为结构清晰、专业易懂的投资报告",
        backstory="""你是一位专业的财经撰稿人，曾为多家知名金融媒体撰写股票分析报告。
        你擅长将复杂的财务和技术数据转化为清晰、结构化的内容，并能突出关键投资要点。
        你的报告简明扼要，重点突出，格式规范，便于投资者快速把握要点。""",
        verbose=True,
        allow_delegation=False
    )

# 创建分析任务
def create_analysis_task(agent, ticker_symbol):
    return Task(
        description=f"""
        对{ticker_symbol}股票进行全面深入的分析，你需要:
        1. 获取并分析公司基本信息（行业、市值、主营业务等）
        2. 分析最新财务数据（收入、利润、现金流等）
        3. 分析技术指标（均线、RSI、MACD等）
        4. 评估市场情绪和新闻影响
        5. 与同行业公司比较
        6. 综合上述因素，给出明确的投资建议（买入/持有/卖出）
        
        分析中应包含量化数据和定性判断，确保全面客观。
        """,
        agent=agent,
        expected_output=f"关于{ticker_symbol}的全面分析结果，包含基本面和技术面数据以及综合评估"
    )

# 创建报告任务
def create_report_task(agent, ticker_symbol):
    return Task(
        description=f"""
        基于股票分析师提供的{ticker_symbol}分析结果，撰写一份专业的投资报告。报告应包含：
        
        1. 报告标题：包含公司名称、当前股价和投资建议
        2. 公司概况：简介公司背景、行业和主要业务
        3. 投资要点：突出3-5个关键投资理由或风险因素
        4. 财务分析：解读关键财务指标及趋势
        5. 技术分析：解读价格走势和技术指标
        6. 风险因素：列出潜在风险和不确定性
        7. 投资建议：给出明确的买入/持有/卖出建议，并注明目标价位
        
        报告格式必须使用Markdown格式，便于在网页中显示。确保报告结构清晰、重点突出，便于快速阅读。
        """,
        agent=agent,
        expected_output=f"一份关于{ticker_symbol}的专业投资报告，采用Markdown格式"
    )

# 分析股票并生成报告
def analyze_stock(ticker_symbol):
    try:
        # 确保 OpenAI 配置完成
        if not setup_openai():
            return "API密钥配置错误，无法进行分析"
            
        # 创建智能体
        analyst = create_stock_analyst_agent()
        writer = create_report_writer_agent()
        
        # 创建任务
        analysis_task = create_analysis_task(analyst, ticker_symbol)
        report_task = create_report_task(writer, ticker_symbol)
        
        # 设置任务依赖关系
        report_task.context = [analysis_task]
        
        # 创建多智能体团队
        crew = Crew(
            agents=[analyst, writer],
            tasks=[analysis_task, report_task],
            verbose=2,
            process=Process.sequential
        )
        
        # 执行分析
        result = crew.kickoff()
        
        return result
    except Exception as e:
        return f"分析过程中出错: {str(e)}"

# 直接运行此文件时显示Streamlit界面
def main():
    # Streamlit界面
    st.set_page_config(
        page_title="多智能体AI股票分析师",
        page_icon="📊",
        layout="wide"
    )

    # 应用标题
    st.title("🤖 多智能体AI股票分析师")
    st.markdown("""
    ### 由双智能体驱动的专业股票分析系统
    本系统由股票分析智能体和报告撰写智能体协作完成分析，提供全面、专业的股票投资报告。
    """)

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

    # 页脚
    st.markdown("---")
    st.markdown("**多智能体AI股票分析师** | 由OpenAI和CrewAI提供支持")

# 当直接运行此文件时
if __name__ == "__main__":
    main() 