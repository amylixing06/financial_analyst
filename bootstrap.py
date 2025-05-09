import os
import sys
import streamlit as st
import importlib

# 应用 SQLite 补丁
try:
    from sqlite_patch import apply_sqlite_patch
    sqlite_patched = apply_sqlite_patch()
except ImportError:
    # 如果无法导入补丁，设置默认环境变量
    sqlite_patched = False
    os.environ["CHROMA_DB_FORCE_DISABLE_VERSION_CHECK"] = "true"

# 设置页面配置
st.set_page_config(
    page_title="多智能体AI股票分析师",
    page_icon="📊",
    layout="wide"
)

# 检查 SQLite 版本并尝试兼容处理
def check_sqlite_version():
    try:
        import sqlite3
        sqlite_version = sqlite3.sqlite_version_info
        required_version = (3, 35, 0)
        
        if sqlite_version < required_version:
            st.warning(f"SQLite 版本 {'.'.join(map(str, sqlite_version))} 低于 ChromaDB 要求的 3.35.0")
            if sqlite_patched:
                st.info("已应用 SQLite 补丁，尝试继续运行完整应用")
                return True
            else:
                st.info("SQLite 版本不兼容，将尝试运行简化版应用")
                return False
        return True
    except Exception as e:
        st.error(f"检查 SQLite 版本时出错: {e}")
        return False

# 安全导入模块，失败则返回 None
def import_module_with_fallback(module_name):
    try:
        return importlib.import_module(module_name)
    except ImportError:
        st.warning(f"无法导入模块 {module_name}")
        return None

# 检查环境并处理潜在问题
def check_environment():
    # 检查 SQLite 版本
    sqlite_ok = check_sqlite_version()
    
    try:
        # 尝试导入基本依赖
        import pandas
        import numpy
        import plotly
        import openai
        
        # 特殊处理 ChromaDB 相关错误
        try:
            # 尝试导入 langchain 相关包
            import_module_with_fallback('langchain')
            import_module_with_fallback('crewai') 
            import_module_with_fallback('langchain_community')
            
            st.success("基础依赖加载成功")
            return True
        except Exception as e:
            if "sqlite3" in str(e).lower():
                st.error(f"SQLite3 版本不兼容: {e}")
                st.info("已尝试绕过 SQLite 版本检查，但仍存在问题。将使用简化版应用。")
                return False
            else:
                st.warning(f"高级依赖加载警告: {e}")
                return sqlite_ok  # 如果 SQLite 版本兼容，但其他依赖有问题，仍可尝试加载完整应用
    except Exception as e:
        st.error(f"基础依赖加载失败: {e}")
        return False

# 检查环境
environment_ok = check_environment()

# 根据环境状态决定加载哪个应用版本
if environment_ok:
    try:
        # 尝试导入完整应用
        from streamlit_app import main as run_main_app
        run_main_app()
    except Exception as e:
        st.error(f"加载完整应用失败: {e}")
        # 回退到简化版
        from simple_app import *
else:
    # 直接使用简化版
    from simple_app import * 