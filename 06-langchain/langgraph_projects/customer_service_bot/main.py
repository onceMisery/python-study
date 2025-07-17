"""
智能客服机器人主入口
- 启动LangGraph工作流，模拟一次完整的客服对话流程
- 适合Python初学者
"""
from graph import run_customer_service_flow

if __name__ == "__main__":
    print("欢迎使用智能客服机器人！")
    run_customer_service_flow() 