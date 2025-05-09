import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from crewai import Tool
from typing import Dict, Any, List, Union
import datetime
import io

class YFinanceStockTool:
    """用于从yfinance API获取股票数据的工具类"""
    
    @staticmethod
    def get_stock_info(ticker_symbol: str) -> Dict[str, Any]:
        """获取股票的基本信息"""
        try:
            ticker = yf.Ticker(ticker_symbol)
            info = ticker.info
            return {
                'longName': info.get('longName', '未知'),
                'sector': info.get('sector', '未知'),
                'industry': info.get('industry', '未知'),
                'website': info.get('website', '未知'),
                'market': info.get('market', '未知'),
                'currentPrice': info.get('currentPrice', info.get('regularMarketPrice', 0)),
                'marketCap': info.get('marketCap', 0),
                'trailingPE': info.get('trailingPE', 0),
                'forwardPE': info.get('forwardPE', 0),
                'dividendYield': info.get('dividendYield', 0) * 100 if info.get('dividendYield') else 0,
                'fiftyTwoWeekHigh': info.get('fiftyTwoWeekHigh', 0),
                'fiftyTwoWeekLow': info.get('fiftyTwoWeekLow', 0),
                'beta': info.get('beta', 0),
                'shortPercentOfFloat': info.get('shortPercentOfFloat', 0),
                'currency': info.get('currency', 'USD'),
                'businessSummary': info.get('longBusinessSummary', '无数据')
            }
        except Exception as e:
            return {'error': f"获取股票信息时出错: {str(e)}"}

    @staticmethod
    def get_historical_data(ticker_symbol: str, period: str = '1y') -> pd.DataFrame:
        """获取历史股价数据
        
        Args:
            ticker_symbol: 股票代码
            period: 时间段 (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)
        """
        try:
            ticker = yf.Ticker(ticker_symbol)
            hist = ticker.history(period=period)
            return hist
        except Exception as e:
            print(f"获取历史数据时出错: {str(e)}")
            return pd.DataFrame()

    @staticmethod
    def get_financial_data(ticker_symbol: str) -> Dict[str, Any]:
        """获取财务数据，包括资产负债表、利润表和现金流量表"""
        try:
            ticker = yf.Ticker(ticker_symbol)
            
            # 获取资产负债表
            balance_sheet = ticker.balance_sheet
            
            # 获取利润表
            income_stmt = ticker.income_stmt
            
            # 获取现金流量表
            cash_flow = ticker.cashflow
            
            # 提取关键指标
            financial_data = {
                '资产负债表': {},
                '利润表': {},
                '现金流量表': {}
            }
            
            # 提取最近的财务数据
            if not balance_sheet.empty and balance_sheet.columns.size > 0:
                recent_bs = balance_sheet[balance_sheet.columns[0]]
                financial_data['资产负债表'] = {
                    '总资产': float(recent_bs.get('Total Assets', 0)),
                    '总负债': float(recent_bs.get('Total Liabilities Net Minority Interest', 0)),
                    '股东权益': float(recent_bs.get('Total Equity Gross Minority Interest', 0)),
                }
            
            if not income_stmt.empty and income_stmt.columns.size > 0:
                recent_is = income_stmt[income_stmt.columns[0]]
                financial_data['利润表'] = {
                    '总收入': float(recent_is.get('Total Revenue', 0)),
                    '毛利润': float(recent_is.get('Gross Profit', 0)),
                    '营业利润': float(recent_is.get('Operating Income', 0)),
                    '净利润': float(recent_is.get('Net Income', 0)),
                }
            
            if not cash_flow.empty and cash_flow.columns.size > 0:
                recent_cf = cash_flow[cash_flow.columns[0]]
                financial_data['现金流量表'] = {
                    '经营活动现金流': float(recent_cf.get('Operating Cash Flow', 0)),
                    '投资活动现金流': float(recent_cf.get('Investing Cash Flow', 0)),
                    '筹资活动现金流': float(recent_cf.get('Financing Cash Flow', 0)),
                    '自由现金流': float(recent_cf.get('Free Cash Flow', 0)),
                }
            
            return financial_data
        except Exception as e:
            return {'error': f"获取财务数据时出错: {str(e)}"}

    @staticmethod
    def calculate_technical_indicators(ticker_symbol: str) -> Dict[str, Any]:
        """计算技术指标，如RSI、MACD和移动平均线"""
        try:
            # 获取历史数据
            df = YFinanceStockTool.get_historical_data(ticker_symbol)
            
            if df.empty:
                return {'error': '无法获取数据来计算技术指标'}
            
            # 计算简单移动平均线 (SMA)
            df['SMA20'] = df['Close'].rolling(window=20).mean()
            df['SMA50'] = df['Close'].rolling(window=50).mean()
            df['SMA200'] = df['Close'].rolling(window=200).mean()
            
            # 计算相对强弱指数 (RSI)
            delta = df['Close'].diff()
            gain = delta.where(delta > 0, 0).rolling(window=14).mean()
            loss = -delta.where(delta < 0, 0).rolling(window=14).mean()
            rs = gain / loss
            df['RSI'] = 100 - (100 / (1 + rs))
            
            # 计算MACD
            exp1 = df['Close'].ewm(span=12, adjust=False).mean()
            exp2 = df['Close'].ewm(span=26, adjust=False).mean()
            df['MACD'] = exp1 - exp2
            df['Signal_Line'] = df['MACD'].ewm(span=9, adjust=False).mean()
            df['MACD_Histogram'] = df['MACD'] - df['Signal_Line']
            
            # 提取最新值
            latest = df.iloc[-1]
            
            result = {
                'current_price': float(latest['Close']),
                'sma20': float(latest['SMA20']),
                'sma50': float(latest['SMA50']),
                'sma200': float(latest['SMA200']),
                'rsi': float(latest['RSI']),
                'macd': float(latest['MACD']),
                'signal_line': float(latest['Signal_Line']),
                'macd_histogram': float(latest['MACD_Histogram']),
                'volume': float(latest['Volume']),
                # 简单的趋势信号
                'trend_signals': {
                    'price_above_sma20': latest['Close'] > latest['SMA20'],
                    'price_above_sma50': latest['Close'] > latest['SMA50'],
                    'price_above_sma200': latest['Close'] > latest['SMA200'],
                    'sma20_above_sma50': latest['SMA20'] > latest['SMA50'],
                    'rsi_oversold': latest['RSI'] < 30,
                    'rsi_overbought': latest['RSI'] > 70,
                    'macd_above_signal': latest['MACD'] > latest['Signal_Line'],
                }
            }
            
            return result
        except Exception as e:
            return {'error': f"计算技术指标时出错: {str(e)}"}

    @staticmethod
    def get_news_sentiment(ticker_symbol: str) -> Dict[str, Any]:
        """模拟获取新闻情绪分析（实际实现中可以使用新闻API）"""
        try:
            # 这里只是模拟数据，实际应用中应连接到新闻API
            return {
                'overall_sentiment': 'neutral',
                'sentiment_score': 0.2,  # 范围从-1(极负面)到1(极正面)
                'news_volume': 'moderate',
                'recent_headlines': [
                    f"最近没有重大{ticker_symbol}相关新闻"
                ]
            }
        except Exception as e:
            return {'error': f"获取新闻情绪时出错: {str(e)}"}

    @staticmethod
    def generate_stock_chart(ticker_symbol: str) -> str:
        """生成股票图表并返回base64编码的图像"""
        try:
            # 获取历史数据
            df = YFinanceStockTool.get_historical_data(ticker_symbol)
            
            if df.empty:
                return ""
            
            # 计算技术指标
            df['SMA20'] = df['Close'].rolling(window=20).mean()
            df['SMA50'] = df['Close'].rolling(window=50).mean()
            
            # 创建Plotly图表
            fig = go.Figure()
            
            # 添加蜡烛图
            fig.add_trace(go.Candlestick(
                x=df.index,
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close'],
                name='K线'
            ))
            
            # 添加移动平均线
            fig.add_trace(go.Scatter(
                x=df.index,
                y=df['SMA20'],
                line=dict(color='blue', width=1.5),
                name='20日均线'
            ))
            
            fig.add_trace(go.Scatter(
                x=df.index,
                y=df['SMA50'],
                line=dict(color='red', width=1.5),
                name='50日均线'
            ))
            
            # 添加成交量
            fig.add_trace(go.Bar(
                x=df.index,
                y=df['Volume'],
                name='成交量',
                marker_color='rgba(0,0,0,0.2)',
                yaxis='y2'
            ))
            
            # 更新布局
            fig.update_layout(
                title=f'{ticker_symbol} 股价走势',
                yaxis_title='价格',
                yaxis2=dict(
                    title='成交量',
                    overlaying='y',
                    side='right'
                ),
                xaxis_rangeslider_visible=False,
                height=600,
                margin=dict(l=50, r=50, b=100, t=100, pad=4),
            )
            
            # 将图表转换为HTML
            buffer = io.StringIO()
            fig.write_html(buffer)
            html_str = buffer.getvalue()
            
            return html_str
        except Exception as e:
            print(f"生成股票图表时出错: {str(e)}")
            return ""

    @staticmethod
    def get_peer_comparison(ticker_symbol: str) -> Dict[str, Any]:
        """获取与同行业公司的比较数据"""
        try:
            ticker = yf.Ticker(ticker_symbol)
            info = ticker.info
            
            # 获取行业信息
            industry = info.get('industry', '')
            sector = info.get('sector', '')
            
            if not industry or not sector:
                return {'error': '无法获取行业信息'}
            
            # 这里只是模拟数据，实际应用中应该查询同行业公司
            return {
                'industry': industry,
                'sector': sector,
                'pe_ratio': info.get('trailingPE', 0),
                'industry_avg_pe': 20.5,  # 模拟数据
                'price_to_book': info.get('priceToBook', 0),
                'industry_avg_pb': 3.2,  # 模拟数据
                'profit_margin': info.get('profitMargin', 0) * 100 if info.get('profitMargin') else 0,
                'industry_avg_profit_margin': 15.3  # 模拟数据
            }
        except Exception as e:
            return {'error': f"获取同行业比较数据时出错: {str(e)}"}

def get_stock_tools() -> List[Tool]:
    """创建并返回一组用于股票分析的工具"""
    stock_tools = [
        Tool(
            name="GetStockInfo",
            description="获取股票的基本信息，如公司名称、行业、当前价格等",
            func=YFinanceStockTool.get_stock_info
        ),
        Tool(
            name="GetHistoricalData",
            description="获取股票的历史价格数据",
            func=YFinanceStockTool.get_historical_data
        ),
        Tool(
            name="GetFinancialData",
            description="获取公司的财务数据，包括资产负债表、利润表和现金流量表",
            func=YFinanceStockTool.get_financial_data
        ),
        Tool(
            name="CalculateTechnicalIndicators",
            description="计算技术指标，如RSI、MACD和移动平均线",
            func=YFinanceStockTool.calculate_technical_indicators
        ),
        Tool(
            name="GetNewsSentiment",
            description="获取与股票相关的新闻情绪分析",
            func=YFinanceStockTool.get_news_sentiment
        ),
        Tool(
            name="GenerateStockChart",
            description="生成股票价格和技术指标的图表",
            func=YFinanceStockTool.generate_stock_chart
        ),
        Tool(
            name="GetPeerComparison",
            description="获取与同行业公司的比较数据",
            func=YFinanceStockTool.get_peer_comparison
        )
    ]
    
    return stock_tools 