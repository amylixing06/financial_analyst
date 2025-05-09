import os
import sys
import streamlit as st
import importlib

# 设置页面配置
st.set_page_config(
    page_title="多智能体AI股票分析师",
    page_icon="📊",
    layout="wide"
)

# 安全导入模块，失败则返回 None
def import_module_with_fallback(module_name):
    try:
        return importlib.import_module(module_name)
    except ImportError:
        st.warning(f"无法导入模块 {module_name}")
        return None
    except Exception as e:
        st.warning(f"导入模块 {module_name} 时出错: {e}")
        return None

# 获取 API 密钥
def get_api_key():
    # 尝试从 Streamlit Secrets 获取
    try:
        return st.secrets["deepseek_api_key"]
    except:
        # 尝试从环境变量获取
        return os.environ.get("DEEPSEEK_API_KEY")

# 检查环境并处理潜在问题
def check_environment():
    # 首先检查API密钥
    api_key = get_api_key()
    if not api_key:
        st.error("未找到DeepSeek API密钥。请在Streamlit Secrets中设置'deepseek_api_key'或设置环境变量'DEEPSEEK_API_KEY'。")
        return False
    
    # 设置环境变量
    os.environ["DEEPSEEK_API_KEY"] = api_key
    
    # 尝试导入简化版分析模块
    simple_analyst = import_module_with_fallback('simple_analyst')
    if simple_analyst:
        st.success("✅ 已加载简化版股票分析模块")
        return True
    
    # 如果无法导入简化版，尝试导入完整版
    # 首先尝试检查是否能导入crewai相关模块
    try:
        import_module_with_fallback('crewai')
        # 如果能导入crewai，尝试导入financial_analyst
        analyst = import_module_with_fallback('financial_analyst')
        if analyst:
            st.success("✅ 已加载完整版股票分析模块")
            return True
    except Exception as e:
        st.warning(f"加载完整版模块时出错: {e}")
    
    # 最后尝试导入极简版
    simple_app = import_module_with_fallback('simple_app')
    if simple_app:
        st.info("已加载极简版应用，某些功能可能受限")
        return False
    
    return False

# 检查环境
environment_ok = check_environment()

if environment_ok:
    try:
        # 优先尝试加载简化版分析模块
        try:
            from simple_analyst import main
            main()
        except ImportError:
            # 如果失败，尝试加载完整版
            try:
                from financial_analyst import main
                main()
            except ImportError:
                st.error("无法加载分析模块，将使用简化版应用")
                from simple_app import *
        except Exception as e:
            st.error(f"加载应用时出错: {str(e)}")
            st.info("尝试加载简化版应用...")
            from simple_app import *
    except Exception as e:
        st.error(f"启动应用时出错: {str(e)}")
        st.info("请联系支持团队")
else:
    # 直接使用极简版
    try:
        from simple_app import *
    except Exception as e:
        st.error(f"加载简化应用时出错: {str(e)}")
        
        # 显示错误信息界面
        st.title("🔧 系统维护中")
        st.markdown("""
        ### 抱歉，应用程序暂时无法使用
        
        我们正在进行系统维护和升级，请稍后再试。如果问题持续，请联系支持团队。
        """)
        
        st.code(f"错误详情: {str(e)}") 