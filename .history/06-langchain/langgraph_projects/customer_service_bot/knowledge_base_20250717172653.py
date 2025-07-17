"""
FAQ知识库检索模块
- 简单文本匹配，适合Python初学者
"""
import os

def faq_search(question):
    """从faqs.txt中查找匹配答案，未找到返回'未找到答案'"""
    path = os.path.join(os.path.dirname(__file__), 'data', 'faqs.txt')
    if not os.path.exists(path):
        return '未找到答案'
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            if not line.strip():
                continue
            q, a = line.strip().split('|', 1)
            if q in question:
                return a
    return '未找到答案' 