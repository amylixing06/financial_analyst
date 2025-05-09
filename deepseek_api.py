import requests
import os
import logging
from typing import Dict, Any, Generator, Optional, List, Union

# 设置日志
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("deepseek_api")

class DeepSeekAPI:
    """DeepSeek API客户端，提供与OpenAI API类似的接口"""
    
    def __init__(self, api_key: str = None, base_url: str = "https://api.deepseek.com"):
        """
        初始化DeepSeek API客户端
        
        Args:
            api_key: DeepSeek API密钥
            base_url: API基础URL，默认为https://api.deepseek.com
        """
        self.api_key = api_key or os.environ.get("DEEPSEEK_API_KEY")
        if not self.api_key:
            raise ValueError("必须提供DeepSeek API密钥")
            
        self.base_url = base_url
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
    
    def chat(self, 
             messages: List[Dict[str, str]], 
             model: str = "deepseek-chat", 
             temperature: float = 0.7,
             max_tokens: int = 1024,
             stream: bool = False,
             **kwargs) -> Union[Dict[str, Any], Generator[Dict[str, Any], None, None]]:
        """
        发送对话请求到DeepSeek API
        
        Args:
            messages: 对话消息列表，格式为[{"role": "user", "content": "你好"}]
            model: 模型名称，可选"deepseek-chat"(DeepSeek-V3)或"deepseek-reasoner"(DeepSeek-R1)
            temperature: 温度参数，控制创造性，范围0-1
            max_tokens: 最大生成令牌数
            stream: 是否使用流式输出
            **kwargs: 其他参数
            
        Returns:
            如果stream=False，返回完整的响应字典
            如果stream=True，返回响应生成器
        """
        url = f"{self.base_url}/chat/completions"
        
        data = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": stream,
            **kwargs
        }
        
        if not stream:
            # 非流式输出
            try:
                response = requests.post(url, headers=self.headers, json=data)
                response.raise_for_status()
                return response.json()
            except Exception as e:
                logger.error(f"请求API时出错: {str(e)}")
                raise
        else:
            # 流式输出
            return self._stream_response(url, data)
    
    def _stream_response(self, url: str, data: Dict[str, Any]) -> Generator[Dict[str, Any], None, None]:
        """
        处理流式响应
        
        Args:
            url: API URL
            data: 请求数据
            
        Returns:
            响应生成器
        """
        try:
            response = requests.post(url, headers=self.headers, json=data, stream=True)
            response.raise_for_status()
            
            for line in response.iter_lines():
                if line:
                    line = line.decode('utf-8')
                    if line.startswith('data: '):
                        if line == 'data: [DONE]':
                            break
                        try:
                            # 去掉'data: '前缀并解析JSON
                            chunk = line[6:]
                            yield json.loads(chunk)
                        except json.JSONDecodeError:
                            continue
        except Exception as e:
            logger.error(f"处理流式响应时出错: {str(e)}")
            raise


class Agent:
    """
    兼容crewai的Agent类接口的简化版本
    """
    def __init__(self, role, goal, backstory, verbose=True, allow_delegation=False, tools=None):
        self.role = role
        self.goal = goal
        self.backstory = backstory
        self.verbose = verbose
        self.allow_delegation = allow_delegation
        self.tools = tools or []


class Task:
    """
    兼容crewai的Task类接口的简化版本
    """
    def __init__(self, description, agent, expected_output, context=None):
        self.description = description
        self.agent = agent
        self.expected_output = expected_output
        self.context = context or []


class Process:
    """
    兼容crewai的Process类接口的简化版本
    """
    sequential = "sequential"


class Crew:
    """
    兼容crewai的Crew类接口的简化版本
    """
    def __init__(self, agents, tasks, verbose=2, process=Process.sequential):
        self.agents = agents
        self.tasks = tasks
        self.verbose = verbose
        self.process = process
        self.deepseek_api = DeepSeekAPI()
    
    def kickoff(self):
        """
        执行任务
        """
        # 创建系统消息
        system_content = f"你是一个多智能体系统。\n\n"
        
        # 添加第一个智能体信息
        analyst = self.agents[0]
        system_content += f"智能体角色：{analyst.role}\n"
        system_content += f"目标：{analyst.goal}\n"
        system_content += f"背景：{analyst.backstory}\n\n"
        
        # 添加第二个智能体信息
        if len(self.agents) > 1:
            writer = self.agents[1]
            system_content += f"智能体角色：{writer.role}\n"
            system_content += f"目标：{writer.goal}\n"
            system_content += f"背景：{writer.backstory}\n\n"
        
        # 添加第一个任务
        first_task = self.tasks[0]
        user_content = f"请执行以下任务：\n{first_task.description}"
        
        messages = [
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_content}
        ]
        
        # 调用DeepSeek API
        response = self.deepseek_api.chat(
            messages=messages,
            model="deepseek-reasoner",  # 使用DeepSeek-R1模型，它更适合复杂推理任务
            temperature=0.7,
            max_tokens=4000,
            stream=False
        )
        
        # 提取回复内容
        first_result = response['choices'][0]['message']['content']
        
        # 如果有第二个任务（报告任务）
        if len(self.tasks) > 1:
            second_task = self.tasks[1]
            
            # 将第一个任务的结果作为上下文
            user_content = f"基于以下分析结果：\n\n{first_result}\n\n请执行以下任务：\n{second_task.description}"
            
            messages = [
                {"role": "system", "content": system_content},
                {"role": "user", "content": user_content}
            ]
            
            # 调用DeepSeek API
            response = self.deepseek_api.chat(
                messages=messages,
                model="deepseek-reasoner",
                temperature=0.7,
                max_tokens=4000,
                stream=False
            )
            
            # 返回最终结果
            return response['choices'][0]['message']['content']
        
        return first_result

import json

# 添加与OpenAI兼容的接口
class OpenAI:
    """提供与OpenAI API兼容的接口类"""
    
    def __init__(self, api_key=None, base_url=None):
        self.api_key = api_key
        self.base_url = base_url
        self.chat = ChatCompletions(api_key, base_url)


class ChatCompletions:
    """聊天完成接口，与OpenAI兼容"""
    
    def __init__(self, api_key=None, base_url=None):
        self.api_key = api_key
        self.base_url = base_url
        self.deepseek_api = DeepSeekAPI(api_key, base_url)
    
    def create(self, model="deepseek-chat", messages=None, stream=False, **kwargs):
        """
        创建聊天完成
        
        Args:
            model: 模型名称
            messages: 消息列表
            stream: 是否流式输出
            **kwargs: 其他参数
        
        Returns:
            如果stream=False，返回完整响应
            如果stream=True，返回流式响应生成器
        """
        return self.deepseek_api.chat(
            model=model,
            messages=messages,
            stream=stream,
            **kwargs
        ) 