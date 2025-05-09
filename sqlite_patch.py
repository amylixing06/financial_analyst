"""
SQLite 版本兼容性补丁

这个模块尝试通过以下方法解决 ChromaDB 需要 SQLite 3.35.0+ 的问题:
1. 尝试导入 pysqlite3 作为 sqlite3 的替代品
2. 如果失败，则设置环境变量绕过 ChromaDB 的版本检查

在 Streamlit Cloud 和其他托管平台上，系统级 SQLite 版本可能比较旧。
"""

import os
import sys
import importlib
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("sqlite_patch")

def apply_sqlite_patch():
    """
    应用 SQLite 补丁以解决版本兼容性问题
    """
    try:
        # 检查当前 SQLite 版本
        import sqlite3
        current_version = sqlite3.sqlite_version_info
        required_version = (3, 35, 0)
        
        if current_version >= required_version:
            logger.info(f"当前 SQLite 版本 {sqlite3.sqlite_version} 已满足要求 (>= 3.35.0)")
            return True
            
        logger.warning(f"当前 SQLite 版本 {sqlite3.sqlite_version} 低于所需版本 3.35.0")
        
        # 尝试方法 1: 使用 pysqlite3 替代
        try:
            logger.info("尝试使用 pysqlite3-binary 替代原生 sqlite3...")
            import pysqlite3
            
            # 替换系统模块
            sys.modules["sqlite3"] = pysqlite3
            
            # 验证补丁是否成功
            import sqlite3
            new_version = sqlite3.sqlite_version_info
            
            if new_version >= required_version:
                logger.info(f"成功: 使用 pysqlite3 版本 {sqlite3.sqlite_version}")
                return True
            else:
                logger.warning(f"pysqlite3 版本仍然过低: {sqlite3.sqlite_version}")
        except ImportError:
            logger.warning("无法导入 pysqlite3-binary 库")
        except Exception as e:
            logger.warning(f"应用 pysqlite3 补丁时出错: {e}")
        
        # 尝试方法 2: 设置环境变量绕过检查
        logger.info("设置环境变量绕过 ChromaDB 版本检查...")
        os.environ["CHROMA_DB_FORCE_DISABLE_VERSION_CHECK"] = "true"
        os.environ["ALLOW_SQLITE_VERSION"] = "true"
        
        return False
    except Exception as e:
        logger.error(f"应用 SQLite 补丁时出错: {e}")
        return False

if __name__ == "__main__":
    # 当脚本直接运行时测试补丁
    result = apply_sqlite_patch()
    print(f"SQLite 补丁应用结果: {'成功' if result else '失败，但已尝试绕过'}") 