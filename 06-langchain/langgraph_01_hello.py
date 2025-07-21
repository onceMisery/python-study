"""
第一个LangGraph程序：Hello, LangGraph!

功能：
- 演示如何用LangGraph创建一个最简单的Agent
- 适合Python初学者，包含详细注释

准备：
- 需先注册OpenAI账号，获取API Key
- 设置环境变量 OPENAI_API_KEY=你的key
- 安装依赖：pip install langgraph langchain openai
"""

import os

from dotenv import load_dotenv
from langgraph.prebuilt import create_react_agent

load_dotenv()

# 初始化大模型
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),  # 使用环境变量获取 API Key
    base_url="https://api.deepseek.com",
    temperature=0,
    model="deepseek-chat"  # 指定模型名称（可选）
)


# 定义一个简单的工具函数
def get_weather(city: str) -> str:
    """获取天气（示例为模拟返回）"""
    return f"{city} 永远阳光明媚！"


# 创建一个ReAct Agent，集成大模型和工具
agent = create_react_agent(
    llm,  # 使用定义好的大模型
    tools=[get_weather],
    prompt="你是一个乐于助人的AI助手"
)

# 执行Agent并获取结果
result = agent.invoke(
    {"messages": [{"role": "user", "content": "北京的天气怎么样？"}]}
)

# 打印AI的回答 -1 是 Python 列表索引的特殊用法，表示最后一个元素。
print("AI回答：", result["messages"][-1].content)
