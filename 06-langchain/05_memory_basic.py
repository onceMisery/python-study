"""
LangChain 记忆（Memory）机制基础示例

功能：
- 用ConversationBufferMemory让AI记住对话历史，实现多轮上下文对话
- 适合Python初学者，包含详细注释

准备：
- 需先注册OpenAI账号，获取API Key
- 设置环境变量 OPENAI_API_KEY=你的key
- 安装依赖：pip install langchain openai
"""
from dotenv import load_dotenv
from langchain.memory import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI
from langchain_core.messages import MessagesPlaceholder
from langchain_core.prompts import ChatPromptTemplate
import os

load_dotenv()

# 初始化 DeepSeek LLM
llm = ChatOpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),  # 使用环境变量获取 API Key
    base_url="https://api.deepseek.com",
    temperature=0.7,
    model="deepseek-chat"  # 指定模型名称（可选）
)

# 创建带有消息历史的提示模板
prompt = ChatPromptTemplate.from_messages(
    [
        MessagesPlaceholder(variable_name="history"),
        ("user", "{input}")
    ]
)

# 创建内存机制
memory = RunnableWithMessageHistory(
    prompt | llm,
    lambda session_id: memory,  # 基于session_id获取对应的记忆
    input_messages_key="input",
    history_messages_key="history"
)

# 多轮对话示例
print(memory.invoke(
    {"input": "你好，请介绍一下LangChain。"},
    config={"configurable": {"session_id": "1"}}
).content)

print(memory.invoke(
    {"input": "它和直接用OpenAI API有什么区别？"},
    config={"configurable": {"session_id": "1"}}
).content)

print(memory.invoke(
    {"input": "能用一句话总结一下吗？"},
    config={"configurable": {"session_id": "1"}}
).content)
