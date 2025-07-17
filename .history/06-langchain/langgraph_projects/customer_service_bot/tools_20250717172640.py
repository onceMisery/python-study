"""
智能客服机器人工具函数
- 工单创建、天气查询等
- 适合Python初学者
"""
import random

def create_ticket(user_id, question):
    """模拟创建工单，返回工单编号"""
    ticket_id = f"T{random.randint(1000,9999)}"
    return ticket_id

def get_weather(city):
    """占位：天气查询，可扩展为真实API"""
    return f"{city} 当前天气晴，温度25°C（模拟数据）" 