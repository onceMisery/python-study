"""
第一个LangChain程序：Hello, LLM!

功能：
- 用LangChain调用OpenAI大模型，完成一次最基础的问答。
- 适合Python初学者，包含详细注释。

准备：
- 需先注册OpenAI账号，获取API Key。
- 设置环境变量 OPENAI_API_KEY=你的key
- 安装依赖：pip install langchain openai
"""
import os

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI

load_dotenv()

# 初始化 DeepSeek LLM
llm = ChatOpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
    temperature=0.7,
    model="deepseek-chat"  # 指定模型名称（可选）
)

# 调用模型 对话描模式
response = llm.invoke([
    {"role": "system", "content": "You are a helpful assistant"},
    {"role": "user", "content": "Hello"},
])

print(response.content)
# 给定角色
response = llm.invoke([HumanMessage("hello")])
print(response.content)