from flask import Flask, Response, request
import os
import subprocess
import sys

app = Flask(__name__)

@app.route('/')
def index():
    # 获取当前目录
    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # 构建命令
    command = [sys.executable, "-m", "streamlit", "run", "financial_analyst.py", "--server.port", "8501", "--server.headless", "true"]
    
    # 设置环境变量
    env = os.environ.copy()
    
    # 执行Streamlit
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=current_dir,
        env=env
    )
    
    # 读取输出
    output, error = process.communicate()
    
    # 如果有错误
    if process.returncode != 0:
        return Response(f"Error: {error.decode('utf-8')}", mimetype="text/plain")
    
    # 返回输出
    return Response(output.decode('utf-8'), mimetype="text/plain")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080))) 