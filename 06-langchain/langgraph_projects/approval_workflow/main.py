"""
AI自动化审批流主入口
- 启动LangGraph审批流，支持批量审批和历史查询
- 适合Python初学者
"""
import json
import os
from graph import run_approval_workflow

def batch_approval():
    requests_path = os.path.join(os.path.dirname(__file__), 'data', 'requests.json')
    with open(requests_path, 'r', encoding='utf-8') as f:
        requests = json.load(f)
    print(f"共读取到{len(requests)}条审批请求，开始批量审批...")
    for req in requests:
        print(f"\n--- 开始审批请求 {req['request_id']} ---")
        run_approval_workflow(init_state=req)
    print("\n全部审批流程已处理完毕。")

def query_history(request_id):
    history_path = os.path.join(os.path.dirname(__file__), 'data', 'history.json')
    if not os.path.exists(history_path):
        print("暂无审批历史记录。")
        return
    with open(history_path, 'r', encoding='utf-8') as f:
        history = json.load(f)
    for record in history:
        if record.get('request_id') == request_id:
            print(f"审批历史：{json.dumps(record, ensure_ascii=False, indent=2)}")
            return
    print(f"未找到请求ID为{request_id}的审批历史。")

if __name__ == "__main__":
    print("欢迎使用AI自动化审批流系统！")
    print("1. 批量审批  2. 查询审批历史  3. 单条演示")
    choice = input("请选择操作（1/2/3）：").strip()
    if choice == '1':
        batch_approval()
    elif choice == '2':
        req_id = input("请输入要查询的审批请求ID：").strip()
        query_history(req_id)
    else:
        run_approval_workflow() 