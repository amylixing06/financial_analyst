import streamlit as st
import os
import yfinance as yf
import json

# 尝试导入自定义的DeepSeek API
try:
    from deepseek_api import DeepSeekAPI
except ImportError:
    # 如果没有，则定义一个简单版本
    import requests
    
    class DeepSeekAPI:
        def __init__(self, api_key=None):
            self.api_key = api_key or os.environ.get("DEEPSEEK_API_KEY")
            self.base_url = "https://api.deepseek.com"
            self.headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
        
        def chat(self, messages, model="deepseek-reasoner", temperature=0.7, max_tokens=4000, **kwargs):
            url = f"{self.base_url}/chat/completions"
            
            data = {
                "model": model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
                **kwargs
            }
            
            response = requests.post(url, headers=self.headers, json=data)
            response.raise_for_status()
            return response.json()

# 设置 Streamlit 页面
st.set_page_config(
    page_title="股票分析师",
    page_icon="📊",
    layout="wide"
)

st.title("🤖 AI股票分析师")
st.markdown("""
### 由DeepSeek AI驱动的股票分析系统
本系统使用DeepSeek AI模型分析股票数据，提供全面、专业的投资分析报告。
""")

# 获取API密钥
def get_api_key():
    # 尝试从 Streamlit Secrets 获取
    try:
        return st.secrets["deepseek_api_key"]
    except:
        # 尝试从环境变量获取
        return os.environ.get("DEEPSEEK_API_KEY")

# 获取股票数据
def get_stock_data(ticker_symbol):
    try:
        ticker = yf.Ticker(ticker_symbol)
        
        # 获取基本信息
        info = ticker.info
        
        # 获取历史价格数据
        hist = ticker.history(period="1y")
        
        # 提取关键数据
        data = {
            "基本信息": {
                "公司名称": info.get("longName", "未知"),
                "行业": info.get("industry", "未知"),
                "市值": info.get("marketCap", "未知"),
                "当前价格": info.get("currentPrice", info.get("regularMarketPrice", "未知")),
            },
            "历史数据": {
                "52周最高": hist["High"].max(),
                "52周最低": hist["Low"].min(),
                "平均交易量": hist["Volume"].mean(),
                "最新收盘价": hist["Close"].iloc[-1],
            }
        }
        
        return data
    except Exception as e:
        return {"错误": str(e)}

# 分析股票
def analyze_stock(ticker_symbol, api_key):
    # 获取股票数据
    stock_data = get_stock_data(ticker_symbol)
    
    # 如果出错，返回错误信息
    if "错误" in stock_data:
        return f"获取股票数据时出错: {stock_data['错误']}"
    
    # 创建 DeepSeek API 客户端
    deepseek = DeepSeekAPI(api_key=api_key)
    
    # 构建提示
    stock_info = json.dumps(stock_data, ensure_ascii=False, indent=2)
    
    system_message = """你是一位专业的股票分析师，需要基于提供的股票数据生成专业的投资分析报告。
报告应该包含以下部分：
1. 报告标题（含股票代码、公司名和投资建议）
2. 公司基本情况
3. 投资要点（3-5个关键点）
4. 技术分析
5. 风险因素
6. 投资建议（明确的买入/持有/卖出建议）

报告应以Markdown格式呈现，便于阅读。"""
    
    user_message = f"""请对股票 {ticker_symbol} 进行专业分析，生成投资报告。
    
股票数据:
{stock_info}

根据这些数据进行分析，给出专业的投资建议。"""
    
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_message}
    ]
    
    # 调用 DeepSeek API
    try:
        response = deepseek.chat(
            messages=messages,
            model="deepseek-reasoner",
            temperature=0.7,
            max_tokens=4000
        )
        
        # 提取回复内容
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"分析过程中出错: {str(e)}"

# 主应用
def main():
    # 获取 API 密钥
    api_key = get_api_key()
    
    if not api_key:
        st.error("未找到DeepSeek API密钥。请在Streamlit Secrets中设置'deepseek_api_key'或设置环境变量'DEEPSEEK_API_KEY'。")
        st.stop()
    
    # API密钥状态显示
    st.success("✅ 已成功加载API密钥")
    
    # 股票代码输入
    with st.form("stock_form"):
        ticker_symbol = st.text_input("输入股票代码 (例如: AAPL, MSFT)", placeholder="AAPL")
        submit_button = st.form_submit_button("分析股票")
    
    # 当用户提交股票代码
    if submit_button and ticker_symbol:
        with st.spinner(f"正在分析 {ticker_symbol} 股票..."):
            report = analyze_stock(ticker_symbol, api_key)
        
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
    st.markdown("**AI股票分析师** | 由DeepSeek AI驱动")

if __name__ == "__main__":
    main() 