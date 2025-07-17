"""
LangGraph 实战项目综合示例

功能：
- 模拟一个智能问答与流程决策的多节点工作流
- 集成大模型、工具、分支、循环和记忆
- 适合Python初学者，包含详细注释

准备：
- 需先注册OpenAI账号，获取API Key
- 设置环境变量 OPENAI_API_KEY=你的key
- 安装依赖：pip install langgraph langchain openai
"""

from langgraph.graph import StateGraph, END
from langchain.llms import OpenAI
from langchain.memory import ConversationBufferMemory

# 1. 定义工具节点（如获取用户信息）
def get_user_info(state):
    print("节点1：获取用户信息")
    # 实际可集成数据库或API，这里模拟
    return {"user": "小明", "age": 25}

# 2. 定义问答节点（集成大模型）
def qa_node(state):
    llm = OpenAI(temperature=0)
    question = state.get("question", "请介绍一下LangGraph")
    print(f"节点2：大模型问答，问题：{question}")
    answer = llm(question)
    return {"qa_answer": answer}

# 3. 定义决策节点（分支）
def decision_node(state):
    age = state.get("age", 0)
    print(f"节点3：决策分支，用户年龄={age}")
    if age >= 18:
        return {"adult": True}
    else:
        return {"adult": False}

# 4. 定义循环节点（模拟多轮对话）
def conversation_node(state):
    memory = state.get("memory")
    if memory is None:
        memory = ConversationBufferMemory()
    llm = OpenAI(temperature=0)
    user_input = state.get("input", "你好，介绍一下LangGraph")
    print(f"节点4：多轮对话，用户输入：{user_input}")
    # 这里只演示一轮，实际可循环
    ai_reply = llm(user_input)
    return {"memory": memory, "last_reply": ai_reply}

# 5. 定义结束节点
def end_node(state):
    print("节点5：流程结束")
    return {"result": "流程已完成，感谢使用！"}

# 6. 构建有向图，集成多种能力
graph = StateGraph()
graph.add_node("get_user", get_user_info)
graph.add_node("qa", qa_node)
graph.add_node("decision", decision_node)
graph.add_node("conversation", conversation_node)
graph.add_node("end", end_node)

graph.add_edge("get_user", "qa")
graph.add_edge("qa", "decision")
graph.add_edge("decision", "conversation", condition=lambda state: state["adult"])  # 成年人进入多轮对话

graph.add_edge("decision", "end", condition=lambda state: not state["adult"])  # 未成年人直接结束

graph.add_edge("conversation", "end")
graph.add_edge("end", END)

# 7. 运行综合项目
print("--- 运行LangGraph实战项目综合示例 ---")
init_state = {"question": "LangGraph和LangChain的区别是什么？", "input": "能再详细说说LangGraph的优势吗？"}
result = graph.invoke(init_state)
print("最终输出：", result) 