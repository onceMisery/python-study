"""
智能客服机器人基础工作流
- 定义LangGraph流程：问候 -> 用户身份检查 -> FAQ检索 -> 工单流转 -> 结束
- 适合Python初学者
"""
from langgraph.graph import StateGraph, END
from knowledge_base import faq_search
from tools import create_ticket
from memory import get_user_profile
from multi_turn import get_conversation_chain
from rag_qa import rag_qa, build_vectorstore

# 1. 问候节点
def greet_node(state):
    print("[问候] 你好，欢迎来到智能客服中心！")
    return state

# 2. 用户身份检查节点
def user_check_node(state):
    user_id = state.get("user_id", "user001")
    profile = get_user_profile(user_id)
    print(f"[身份] 用户ID: {user_id}, 用户画像: {profile}")
    state["profile"] = profile
    return state

# 3. FAQ检索节点（扩展RAG）
def faq_node(state):
    question = state.get("question", "如何重置密码？")
    answer = faq_search(question)
    print(f"[FAQ] 用户问题: {question}\n[FAQ] 匹配答案: {answer}")
    state["faq_answer"] = answer
    # FAQ未命中时，自动进入RAG知识库检索
    if answer == "未找到答案":
        print("[RAG] FAQ未命中，进入知识库检索...")
        vectorstore = state.get("vectorstore")
        if vectorstore is None:
            vectorstore = build_vectorstore()
            state["vectorstore"] = vectorstore
        rag_answer = rag_qa(question, vectorstore)
        print(f"[RAG] 检索答案: {rag_answer}")
        state["rag_answer"] = rag_answer
    return state

# 4. 工单流转节点
def ticket_node(state):
    if state.get("faq_answer") == "未找到答案":
        ticket_id = create_ticket(state.get("user_id", "user001"), state.get("question", ""))
        print(f"[工单] 已为您创建工单，编号: {ticket_id}")
        state["ticket_id"] = ticket_id
    else:
        print("[工单] 无需创建工单，已找到FAQ答案")
    return state

# 5. 结束节点
def end_node(state):
    print("[结束] 感谢您的咨询，祝您生活愉快！")
    return state

# 6. 多轮对话节点
def multi_turn_node(state):
    memory = state.get("memory")
    chain, memory = get_conversation_chain(memory)
    user_input = state.get("multi_input", "请介绍一下智能客服机器人")
    print(f"[多轮对话] 用户输入: {user_input}")
    ai_reply = chain.predict(input=user_input)
    print(f"[多轮对话] AI回复: {ai_reply}")
    state["memory"] = memory
    state["multi_reply"] = ai_reply
    return state

# 6. 构建工作流
def run_customer_service_flow():
    graph = StateGraph()
    graph.add_node("greet", greet_node)
    graph.add_node("user_check", user_check_node)
    graph.add_node("faq", faq_node)
    graph.add_node("ticket", ticket_node)
    graph.add_node("multi_turn", multi_turn_node)
    graph.add_node("end", end_node)

    graph.add_edge("greet", "user_check")
    graph.add_edge("user_check", "faq")
    graph.add_edge("faq", "ticket")
    graph.add_edge("ticket", "multi_turn")
    graph.add_edge("multi_turn", "end")
    graph.add_edge("end", END)

    # 启动流程，支持多轮输入
    memory = None
    multi_inputs = [
        "请介绍一下智能客服机器人",
        "它支持哪些功能？",
        "能用一句话总结一下吗？"
    ]
    state = {
        "user_id": "user001",
        "question": "如何重置密码？",
        "memory": memory
    }
    for user_input in multi_inputs:
        state["multi_input"] = user_input
        state = graph.invoke(state) 