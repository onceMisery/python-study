"""
用户画像与上下文记忆管理
- 适合Python初学者
"""
import json
import os

def get_user_profile(user_id):
    """模拟从本地文件读取用户画像"""
    path = os.path.join(os.path.dirname(__file__), 'data', 'users.json')
    if not os.path.exists(path):
        # 默认用户画像
        return {"user_id": user_id, "name": "小明", "vip": False}
    with open(path, 'r', encoding='utf-8') as f:
        users = json.load(f)
    return users.get(user_id, {"user_id": user_id, "name": "小明", "vip": False}) 