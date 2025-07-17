"""
多Agent协作模块
- 定义FAQAgent、RAGAgent、ToolAgent、TicketAgent
- 适合Python初学者
"""
from knowledge_base import faq_search
from rag_qa import rag_qa, build_vectorstore
from tools import get_weather, query_express, create_ticket

# FAQ专家Agent
def faq_agent(question):
    answer = faq_search(question)
    return answer

# RAG专家Agent
def rag_agent(question, vectorstore=None):
    return rag_qa(question, vectorstore)

# 工具专家Agent
def tool_agent(question, city=None, express_no=None):
    if "天气" in question:
        return get_weather(city or "北京")
    elif "快递" in question:
        return query_express(express_no or "1234567890")
    else:
        return "未识别到可用工具"

# 工单专员Agent
def ticket_agent(user_id, question):
    return create_ticket(user_id, question) 