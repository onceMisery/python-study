"""
LangGraph 集成大模型与工具基础示例

功能：
- 演示如何在节点中调用大模型（OpenAI）和自定义工具
- 适合Python初学者，包含详细注释

准备：
- 需先注册OpenAI账号，获取API Key
- 设置环境变量 OPENAI_API_KEY=你的key
- 安装依赖：pip install langgraph langchain openai
"""

from langgraph.graph import StateGraph, END
from langchain.llms import OpenAI

# 1. 定义自定义工具函数
def get_python_version(state):
    import sys
    version = sys.version.split()[0]
    print(f"工具：当前Python版本为{version}")
    return {"python_version": version}

# 2. 定义大模型节点
def ask_llm(state):
    llm = OpenAI(temperature=0)
    question = state.get("question", "介绍一下LangGraph")
    print(f"节点：调用大模型回答问题：{question}")
    answer = llm(question)
    return {"llm_answer": answer}

# 3. 构建有向图，集成工具和大模型
graph = StateGraph()
graph.add_node("tool", get_python_version)
graph.add_node("llm", ask_llm)

graph.add_edge("tool", "llm")
graph.add_edge("llm", END)

# 4. 运行图
init_state = {"question": "请用一句话介绍LangGraph的作用"}
result = graph.invoke(init_state)
print("最终输出：", result) 