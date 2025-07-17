"""
LangGraph 多轮对话Agent基础示例

功能：
- 用LangGraph实现带记忆的多轮对话Agent，集成大模型和Memory
- 适合Python初学者，包含详细注释

准备：
- 需先注册OpenAI账号，获取API Key
- 设置环境变量 OPENAI_API_KEY=你的key
- 安装依赖：pip install langgraph langchain openai
"""

from langgraph.graph import StateGraph, END
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain.llms import OpenAI

# 1. 定义带记忆的多轮对话节点
def chat_node(state):
    # ConversationBufferMemory会自动记录对话历史
    memory = state.get("memory")
    if memory is None:
        memory = ConversationBufferMemory()
    llm = OpenAI(temperature=0)
    chain = ConversationChain(llm=llm, memory=memory, verbose=True)
    user_input = state.get("input", "你好，请介绍一下LangGraph。")
    print(f"用户输入：{user_input}")
    ai_reply = chain.predict(input=user_input)
    # 更新记忆对象到state，便于多轮对话
    return {"memory": chain.memory, "last_reply": ai_reply}

# 2. 构建有向图，支持多轮对话
graph = StateGraph()
graph.add_node("chat", chat_node)
graph.add_edge("chat", END)

# 3. 运行多轮对话
memory = ConversationBufferMemory()
inputs = [
    "你好，请介绍一下LangGraph。",
    "它和LangChain有什么关系？",
    "能用一句话总结一下吗？"
]

for i, user_input in enumerate(inputs, 1):
    print(f"\n--- 第{i}轮对话 ---")
    result = graph.invoke({"input": user_input, "memory": memory})
    memory = result["memory"]
    print("AI回复：", result["last_reply"]) 