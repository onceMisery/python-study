"""
LangGraph 集成大模型与工具基础示例

功能：
- 演示如何在节点中调用大模型（OpenAI）和自定义工具
- 适合Python初学者，包含详细注释

准备：
- 需先注册DeepSeek账号，获取API Key
- 设置环境变量 DEEPSEEK_API_KEY=你的key
- 安装依赖：pip install langgraph langchain langchain-openai
"""

import io
# 在文件开头添加
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 添加清理函数
def clean_response(text):
    return text.replace("\uFFFD", "").strip()

# 1. 导入必要的库
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
import os

# 2. 初始化大模型
load_dotenv()
llm = ChatOpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),  # 使用环境变量获取 API Key
    base_url="https://api.deepseek.com",
    temperature=0,
    model="deepseek-chat"  # 指定模型名称（可选）
)

# 3. 定义状态类
from typing import TypedDict

class State(TypedDict):
    question: str
    python_version: str
    llm_answer: str

# 4. 定义自定义工具函数
def get_python_version(state: State):
    import sys
    version = sys.version.split()[0]
    print(f"工具：当前Python版本为{version}")
    return {"python_version": version}

# 5. 定义大模型节点
def ask_llm(state: State):
    print(f"节点：调用大模型回答问题：{state.get('question', '介绍一下LangGraph')}")
    question = clean_response(state.get("question", "介绍一下LangGraph"))
    response = llm.invoke(question)
    return {"llm_answer": response.content}

# 6. 构建有向图，集成工具和大模型
graph = StateGraph(state_schema=State)
graph.add_node("tool", get_python_version)
graph.add_node("llm", ask_llm)

graph.add_edge("tool", "llm")
graph.add_edge("llm", END)

# 设置入口节点
graph.set_entry_point("tool")

# 7. 运行图
app = graph.compile()
init_state = {"question": "请用一句话介绍LangGraph的作用"}
result = app.invoke(init_state)
print("最终输出：", result)
