"""
AI自动化审批流各类节点与业务逻辑
- 适合Python初学者
"""
from integrations import send_notification, send_email, send_erp_update, send_alert
import json
import os

# 1. 用户提交节点
def submit_node(state):
    print(f"[提交] 用户: {state['user']}，金额: {state['amount']}，事由: {state['reason']}，紧急: {state['urgent']}")
    return state

# 2. 主管审批节点（支持异常监控）
def manager_approve_node(state):
    approver = get_approver("manager")
    print(f"[主管审批] {approver} 审批中...")
    try:
        # 模拟异常
        if state.get('simulate_error') == 'manager':
            raise Exception("主管审批异常！")
        state['manager_approved'] = True
        state['manager_comment'] = "同意，理由合理。"
        state['manager_approver'] = approver
    except Exception as e:
        send_alert(f"主管审批节点异常：{e}")
        state['manager_approved'] = False
        state['manager_comment'] = str(e)
    return state

# 3. 金额判断分支节点
def amount_branch_node(state):
    print(f"[分支] 审批金额: {state['amount']}")
    return state

# 4. 财务审批节点（支持动态审批人）
def finance_approve_node(state):
    approver = get_approver("finance")
    print(f"[财务审批] {approver} 审批中...")
    state['finance_approved'] = True
    state['finance_comment'] = "预算充足，同意。"
    state['finance_approver'] = approver
    return state

# 5. 总经理审批节点（支持动态审批人）
def ceo_approve_node(state):
    approver = get_approver("ceo")
    print(f"[总经理审批] {approver} 审批中...")
    state['ceo_approved'] = True
    state['ceo_comment'] = "同意采购，尽快执行。"
    state['ceo_approver'] = approver
    return state

# 6. 通知节点
def notify_node(state):
    print("[通知] 正在发送审批结果通知...")
    send_notification(state['user'], f"您的审批请求({state['request_id']})已通过！")
    return state

# 7. 结束节点（审批通过/拒绝后自动推送消息或写入外部系统）
def end_node(state):
    print("[结束] 审批流程已完成，感谢使用！")
    # 写入审批历史
    history_path = os.path.join(os.path.dirname(__file__), 'data', 'history.json')
    if os.path.exists(history_path):
        with open(history_path, 'r', encoding='utf-8') as f:
            history = json.load(f)
    else:
        history = []
    record = {k: v for k, v in state.items() if isinstance(v, (str, int, float, bool, type(None)))}
    history.append(record)
    with open(history_path, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)
    print(f"[历史] 已写入审批历史记录（共{len(history)}条）")
    # 审批通过/拒绝后自动推送
    status = "通过" if state.get('manager_approved') else "拒绝"
    send_email(state.get('user', ''), f"审批结果通知", f"您的审批请求({state.get('request_id')})已{status}")
    send_erp_update(state.get('request_id'), status)
    return state

# 并发审批节点（模拟会签）
def parallel_approve_node(state):
    print("[并发审批] 财务和总经理并行审批（模拟）...")
    # 并发审批结果汇总
    state = finance_approve_node(state)
    state = ceo_approve_node(state)
    state['parallel_approved'] = state['finance_approved'] and state['ceo_approved']
    return state

# 动态获取审批人
def get_approver(role):
    rules_path = os.path.join(os.path.dirname(__file__), 'data', 'rules.json')
    if not os.path.exists(rules_path):
        return role
    with open(rules_path, 'r', encoding='utf-8') as f:
        rules = json.load(f)
    return rules.get('approvers', {}).get(role, role) 