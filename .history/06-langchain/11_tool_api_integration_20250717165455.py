"""
LangChain 与外部API集成基础示例

功能：
- 自定义工具让AI在对话中自动调用外部API（如获取天气信息）
- 适合Python初学者，包含详细注释

准备：
- 需先注册OpenAI账号，获取API Key
- 设置环境变量 OPENAI_API_KEY=你的key
- 安装依赖：pip install langchain openai requests
"""

from langchain.tools import tool
from langchain.agents import initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI
import requests

# 定义一个外部API工具（以获取天气为例，实际可替换为任意API）
@tool
def get_weather(city: str) -> str:
    """获取指定城市的天气信息（示例为模拟返回，实际可接入真实API）"""
    # 这里用模拟数据，实际可用 requests.get 调用真实API
    # resp = requests.get(f"https://api.weatherapi.com/v1/current.json?key=你的key&q={city}")
    # data = resp.json()
    # return f"{city} 当前温度: {data['current']['temp_c']}°C"
    return f"{city} 当前天气晴，温度25°C（模拟数据）"

# 初始化大模型
llm = ChatOpenAI(temperature=0)

# 工具列表
tools = [get_weather]

# 初始化Agent，支持工具调用
agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.OPENAI_FUNCTIONS,
    verbose=True
)

# 让AI自动决定是否调用API工具
print(agent.run("请查询一下北京的天气"))
print(agent.run("再查一下上海的天气")) 