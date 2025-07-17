"""
LangGraph 与 LangSmith 调试基础示例

功能：
- 演示如何集成LangSmith，对LangGraph工作流进行链路追踪和调试
- 适合Python初学者，包含详细注释

准备：
- 需先注册OpenAI账号，获取API Key
- 需注册LangSmith账号，获取LANGCHAIN_API_KEY
- 设置环境变量 OPENAI_API_KEY=你的key
- 设置环境变量 LANGCHAIN_API_KEY=你的key
- 安装依赖：pip install langgraph langchain openai langsmith
"""

from langgraph.graph import StateGraph, END
from langsmith import traceable
import os

# 1. 定义可追踪的节点函数
@traceable
def add_node(state):
    print("节点1：加法运算")
    a = state.get("a", 1)
    b = state.get("b", 2)
    return {"sum": a + b}

@traceable
def mul_node(state):
    print("节点2：乘法运算")
    s = state["sum"]
    return {"result": s * 10}

# 2. 构建有向图，集成LangSmith追踪
graph = StateGraph()
graph.add_node("add", add_node)
graph.add_node("mul", mul_node)
graph.add_edge("add", "mul")
graph.add_edge("mul", END)

# 3. 运行工作流（可在LangSmith平台查看链路追踪）
print("--- 运行带LangSmith调试的工作流 ---")
result = graph.invoke({"a": 3, "b": 5})
print("最终输出：", result)

# 说明：
# 1. 需在 https://smith.langchain.com/ 注册账号并获取API Key
# 2. 运行后可在LangSmith平台查看详细链路追踪和调试信息 