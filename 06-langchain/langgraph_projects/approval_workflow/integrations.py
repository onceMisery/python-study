"""
外部系统集成模块
- 模拟消息/邮件通知
- 适合Python初学者
"""
def send_notification(user, message):
    print(f"[通知] 已向用户 {user} 发送消息：{message}")

def send_email(to, subject, content):
    print(f"[邮件] 向 {to} 发送邮件：{subject} | 内容：{content}")
    # 可扩展为真实邮件API

def send_erp_update(request_id, status):
    print(f"[ERP] 更新ERP系统审批单 {request_id} 状态为：{status}")
    # 可扩展为真实ERP API

def send_alert(message):
    print(f"[告警] {message}")
    # 可扩展为企业微信/钉钉/短信等告警API 