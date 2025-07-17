"""
AI自动化审批流基础工作流
- 定义LangGraph流程：用户提交 -> 主管审批 -> 金额判断分支 -> 财务/总经理审批 -> 通知 -> 结束
- 适合Python初学者
"""
from langgraph.graph import StateGraph, END
from nodes import submit_node, manager_approve_node, amount_branch_node, finance_approve_node, ceo_approve_node, notify_node, end_node

def run_approval_workflow():
    graph = StateGraph()
    graph.add_node("submit", submit_node)
    graph.add_node("manager", manager_approve_node)
    graph.add_node("amount_branch", amount_branch_node)
    graph.add_node("finance", finance_approve_node)
    graph.add_node("ceo", ceo_approve_node)
    graph.add_node("notify", notify_node)
    graph.add_node("end", end_node)

    graph.add_edge("submit", "manager")
    graph.add_edge("manager", "amount_branch")
    graph.add_edge("amount_branch", "finance", condition=lambda state: state["amount"] < 10000)
    graph.add_edge("amount_branch", "ceo", condition=lambda state: state["amount"] >= 10000)
    graph.add_edge("finance", "notify")
    graph.add_edge("ceo", "notify")
    graph.add_edge("notify", "end")
    graph.add_edge("end", END)

    # 启动流程，模拟一次审批
    init_state = {
        "request_id": "REQ001",
        "user": "张三",
        "amount": 12000,
        "reason": "采购高性能服务器",
        "urgent": True
    }
    graph.invoke(init_state) 