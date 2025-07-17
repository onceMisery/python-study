"""
LangChain 工具调用（Tool Calling）基础示例

功能：
- 让大模型在对话中自动调用自定义函数（工具），实现“AI+工具”能力
- 适合Python初学者，包含详细注释

准备：
- 需先注册OpenAI账号，获取API Key
- 设置环境变量 OPENAI_API_KEY=你的key
- 安装依赖：pip install langchain openai
"""

from langchain.tools import tool
from langchain.agents import initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI

# 定义一个自定义工具（函数）
@tool
def get_python_version() -> str:
    """返回当前Python的主版本号。"""
    import sys
    return f"当前Python主版本号: {sys.version_info.major}"

# 初始化大模型
llm = ChatOpenAI(temperature=0)

# 工具列表
tools = [get_python_version]

# 初始化Agent，支持工具调用
agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.OPENAI_FUNCTIONS,
    verbose=True
)

# 让AI自动决定是否调用工具
result = agent.run("请告诉我当前Python的主版本号是多少？")
print("AI回答：", result) 