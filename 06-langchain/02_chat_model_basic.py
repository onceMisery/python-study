"""
LangChain 聊天模型基础示例

功能：
- 用LangChain调用OpenAI的Chat模型（如gpt-3.5/4），实现多轮对话
- 展示与基础LLM的区别
- 适合Python初学者，包含详细注释

准备：
- 需先注册OpenAI账号，获取API Key
- 设置环境变量 OPENAI_API_KEY=你的key
- 安装依赖：pip install langchain openai
"""

from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    SystemMessage,
    HumanMessage,
    AIMessage
)

# 初始化ChatOpenAI模型
chat = ChatOpenAI(temperature=0.7)

# 构建对话历史
messages = [
    SystemMessage(content="你是一个专业的Python学习助手。"),
    HumanMessage(content="什么是LangChain？"),
    AIMessage(content="LangChain是一个用于构建基于大语言模型的AI应用开发框架。"),
    HumanMessage(content="它和直接用OpenAI API有什么区别？")
]

# 发送多轮对话
response = chat(messages)

print("AI回答：", response.content) 