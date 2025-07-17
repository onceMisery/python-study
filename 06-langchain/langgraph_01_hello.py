"""
第一个LangGraph程序：Hello, LangGraph!

功能：
- 演示如何用LangGraph创建一个最简单的Agent
- 适合Python初学者，包含详细注释

准备：
- 需先注册OpenAI账号，获取API Key
- 设置环境变量 OPENAI_API_KEY=你的key
- 安装依赖：pip install langgraph langchain openai
"""

from langgraph.prebuilt import create_react_agent

# 定义一个简单的工具函数
def get_weather(city: str) -> str:
    """获取天气（示例为模拟返回）"""
    return f"{city} 永远阳光明媚！"

# 创建一个ReAct Agent，集成大模型和工具
agent = create_react_agent(
    model="openai:gpt-3.5-turbo",  # 你也可以用 "openai:gpt-4"
    tools=[get_weather],
    prompt="你是一个乐于助人的AI助手"
)

# 运行Agent，进行一次对话
result = agent.invoke(
    {"messages": [{"role": "user", "content": "北京的天气怎么样？"}]}
)
print("AI回答：", result["messages"][-1]["content"]) 