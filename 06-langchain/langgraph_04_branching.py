import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def clean_response(text):
    return text.replace("\uFFFD", "").strip()

"""
LangGraph 状态管理与分支基础示例

功能：
- 演示如何根据状态条件实现流程分支（if/else逻辑）
- 适合Python初学者，包含详细注释

准备：
- 需先注册DeepSeek账号，获取API Key
- 设置环境变量 DEEPSEEK_API_KEY=你的key
- 安装依赖：pip install langgraph langchain langchain-openai
"""

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
    score: int
    result: str

# 4. 定义节点函数
def check_score(state: State):
    score = state.get("score", 0)
    print(f"节点1：检查分数，当前分数={score}")
    return {"score": score}


def pass_node(state: State):
    print("节点2：分支-及格")
    response = llm.invoke(f"分数为{state['score']}，生成一份祝贺信息")
    return {"result": clean_response(response.content)}


def fail_node(state: State):
    print("节点3：分支-不及格")
    response = llm.invoke(f"分数为{state['score']}，生成一份鼓励信息")
    return {"result": clean_response(response.content)}

# 5. 构建有向图，添加分支逻辑
graph = StateGraph(state_schema=State)
graph.add_node("check", check_score)
graph.add_node("pass", pass_node)
graph.add_node("fail", fail_node)

# 添加条件边
graph.add_conditional_edges(
    source="check",
    path=lambda state: "pass" if state["score"] >= 60 else "fail",
    path_map=["pass", "fail"]
)
graph.add_edge("pass", END)
graph.add_edge("fail", END)

# 设置入口节点
graph.set_entry_point("check")

# 6. 运行图，测试不同分数
app = graph.compile()

print("--- 测试及格分支 ---")
result1 = app.invoke({"score": 85})
print("最终输出：", result1)

print("\n--- 测试不及格分支 ---")
result2 = app.invoke({"score": 45})
print("最终输出：", result2)
