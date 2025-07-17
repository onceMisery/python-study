"""
多轮对话与上下文记忆模块
- 基于LangChain ConversationChain
- 适合Python初学者
"""
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.llms import OpenAI

# 创建多轮对话链对象
def get_conversation_chain(memory=None):
    if memory is None:
        memory = ConversationBufferMemory()
    llm = OpenAI(temperature=0)
    chain = ConversationChain(llm=llm, memory=memory, verbose=True)
    return chain, memory 