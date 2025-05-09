# 这是 Streamlit Cloud 默认寻找的入口文件
# 直接导入 financial_analyst.py 中的全部内容

# 导入必要的库
import streamlit as st
import os
import json
from dotenv import load_dotenv

# 导入 financial_analyst.py 中的功能
from financial_analyst import *

# 注意：由于 financial_analyst.py 中已经包含了 Streamlit 界面代码
# 导入该模块时会自动运行其中的 Streamlit 应用 