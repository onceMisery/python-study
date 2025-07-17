"""
LangChain 多轮对话Agent基础示例

功能：
- 结合Agent、Memory和Tool Calling，实现带记忆的多轮对话与工具调用
- 适合Python初学者，包含详细注释

准备：
- 需先注册OpenAI账号，获取API Key
- 设置环境变量 OPENAI_API_KEY=你的key
- 安装依赖：pip install langchain openai tiktoken faiss-cpu
"""

from langchain.tools import tool
from langchain.agents import initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory

# 定义一个自定义工具
@tool
def get_python_version() -> str:
    """返回当前Python的主版本号。"""
    import sys
    return f"当前Python主版本号: {sys.version_info.major}"

# 初始化大模型
llm = ChatOpenAI(temperature=0)

# 工具列表
tools = [get_python_version]

# 创建对话记忆对象
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# 初始化Agent，支持工具调用和记忆
agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.OPENAI_FUNCTIONS,
    memory=memory,
    verbose=True
)

# 多轮对话示例
print(agent.run("你好，请记住我叫小明。"))
print(agent.run("我刚才让你记住了什么？"))
print(agent.run("请告诉我当前Python的主版本号。"))
print(agent.run("我叫什么名字？")) 