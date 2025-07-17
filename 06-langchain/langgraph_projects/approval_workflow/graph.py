"""
AI自动化审批流基础工作流
- 定义LangGraph流程：用户提交 -> 主管审批 -> 金额判断分支 -> 财务/总经理审批 -> 通知 -> 结束
- 适合Python初学者
"""
from langgraph.graph import StateGraph, END
from nodes import submit_node, manager_approve_node, amount_branch_node, finance_approve_node, ceo_approve_node, notify_node, end_node, parallel_approve_node
import json
import os

def export_mermaid():
    """导出审批流为Mermaid流程图"""
    mermaid = ["graph TD"]
    mermaid.append("submit[用户提交] --> manager[主管审批]")
    mermaid.append("manager --> amount_branch[金额判断]")
    mermaid.append("amount_branch -- 小于阈值 --> finance[财务审批]")
    mermaid.append("amount_branch -- 大于等于阈值 --> ceo[总经理审批]")
    mermaid.append("finance --> notify[通知]")
    mermaid.append("ceo --> notify")
    mermaid.append("notify --> end[结束]")
    with open(os.path.join(os.path.dirname(__file__), 'approval_flow.mmd'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(mermaid))
    print("[可视化] 已导出审批流Mermaid流程图：approval_flow.mmd")

def build_graph_from_dsl(flow_path):
    """根据flow.json配置动态生成审批流"""
    import importlib
    with open(flow_path, 'r', encoding='utf-8') as f:
        flow = json.load(f)
    graph = StateGraph()
    # 动态添加节点
    for node in flow['nodes']:
        node_id = node['id']
        # 节点函数名与id一致，或可自定义映射
        func = getattr(importlib.import_module('nodes'), f"{node_id}_node", None)
        if func:
            graph.add_node(node_id, func)
    # 动态添加边
    for edge in flow['edges']:
        from_id = edge['from']
        to_id = edge['to']
        cond = edge.get('condition')
        if cond:
            # 仅支持简单表达式，实际可用eval/ast.literal_eval等
            graph.add_edge(from_id, to_id, condition=lambda state, c=cond: eval(c, {}, state))
        else:
            graph.add_edge(from_id, to_id)
    graph.add_edge(flow['nodes'][-1]['id'], END)
    return graph

def run_approval_workflow(init_state=None, use_dsl=False):
    # 动态读取规则
    rules_path = os.path.join(os.path.dirname(__file__), 'data', 'rules.json')
    if os.path.exists(rules_path):
        with open(rules_path, 'r', encoding='utf-8') as f:
            rules = json.load(f)
        amount_threshold = rules.get('amount_threshold', 10000)
    else:
        amount_threshold = 10000

    if use_dsl:
        flow_path = os.path.join(os.path.dirname(__file__), 'data', 'flow.json')
        graph = build_graph_from_dsl(flow_path)
    else:
        graph = StateGraph()
        graph.add_node("submit", submit_node)
        graph.add_node("manager", manager_approve_node)
        graph.add_node("amount_branch", amount_branch_node)
        graph.add_node("finance", finance_approve_node)
        graph.add_node("ceo", ceo_approve_node)
        graph.add_node("parallel", parallel_approve_node)
        graph.add_node("notify", notify_node)
        graph.add_node("end", end_node)

        graph.add_edge("submit", "manager")
        graph.add_edge("manager", "amount_branch")
        graph.add_edge("amount_branch", "finance", condition=lambda state: state["amount"] < amount_threshold)
        graph.add_edge("amount_branch", "ceo", condition=lambda state: state["amount"] >= amount_threshold and not state.get("urgent"))
        graph.add_edge("amount_branch", "parallel", condition=lambda state: state["amount"] >= amount_threshold and state.get("urgent"))
        graph.add_edge("finance", "notify")
        graph.add_edge("ceo", "notify")
        graph.add_edge("parallel", "notify")
        graph.add_edge("notify", "end")
        graph.add_edge("end", END)

    # 启动流程，支持传入初始状态
    if init_state is None:
        init_state = {
            "request_id": "REQ001",
            "user": "张三",
            "amount": 12000,
            "reason": "采购高性能服务器",
            "urgent": True
        }
    graph.invoke(init_state) 