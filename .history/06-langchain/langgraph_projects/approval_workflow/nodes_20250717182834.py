"""
AI自动化审批流各类节点与业务逻辑
- 适合Python初学者
"""
from integrations import send_notification
import json
import os

# 1. 用户提交节点
def submit_node(state):
    print(f"[提交] 用户: {state['user']}，金额: {state['amount']}，事由: {state['reason']}，紧急: {state['urgent']}")
    return state

# 2. 主管审批节点
def manager_approve_node(state):
    print("[主管审批] 部门主管审批中...")
    # 模拟主管审批意见
    state['manager_approved'] = True
    state['manager_comment'] = "同意，理由合理。"
    return state

# 3. 金额判断分支节点
def amount_branch_node(state):
    print(f"[分支] 审批金额: {state['amount']}")
    return state

# 4. 财务审批节点
def finance_approve_node(state):
    print("[财务审批] 财务审批中...")
    state['finance_approved'] = True
    state['finance_comment'] = "预算充足，同意。"
    return state

# 5. 总经理审批节点
def ceo_approve_node(state):
    print("[总经理审批] 总经理审批中...")
    state['ceo_approved'] = True
    state['ceo_comment'] = "同意采购，尽快执行。"
    return state

# 6. 通知节点
def notify_node(state):
    print("[通知] 正在发送审批结果通知...")
    send_notification(state['user'], f"您的审批请求({state['request_id']})已通过！")
    return state

# 7. 结束节点
def end_node(state):
    print("[结束] 审批流程已完成，感谢使用！")
    # 写入审批历史
    history_path = os.path.join(os.path.dirname(__file__), 'data', 'history.json')
    if os.path.exists(history_path):
        with open(history_path, 'r', encoding='utf-8') as f:
            history = json.load(f)
    else:
        history = []
    # 只保留可序列化字段
    record = {k: v for k, v in state.items() if isinstance(v, (str, int, float, bool, type(None)))}
    history.append(record)
    with open(history_path, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)
    print(f"[历史] 已写入审批历史记录（共{len(history)}条）")
    return state 