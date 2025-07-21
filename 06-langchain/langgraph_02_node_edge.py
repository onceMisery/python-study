"""
LangGraph 节点（Node）与边（Edge）基础示例

功能：
- 演示如何自定义节点函数，构建简单的有向图（Graph）
- 适合Python初学者，包含详细注释

准备：
- 需先注册OpenAI账号，获取API Key
- 设置环境变量 OPENAI_API_KEY=你的key
- 安装依赖：pip install langgraph langchain openai
"""
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
import os

load_dotenv()

# 初始化大模型
llm = ChatOpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),  # 使用环境变量获取 API Key
    base_url="https://api.deepseek.com",
    temperature=0,
    model="deepseek-chat"  # 指定模型名称（可选）
)

# 1. 定义节点函数（每个节点就是一个Python函数）
def greet(state):
    print("节点1：问候用户")
    # 使用大模型生成问候语
    response = llm.invoke("用中文写一句友好的欢迎语")
    print("Greet response:", response.content)  # 添加调试输出
    return {"greet": response.content}


def ask_name(state):
    print("节点2：询问用户姓名")
    # 使用大模型生成询问语
    response = llm.invoke("用中文写一句自然的询问用户姓名的话")
    print("Ask name response:", response.content)  # 添加调试输出
    return {"name": input(response.content)}


def say_goodbye(state):
    print("节点3：结束对话")
    # 使用大模型生成告别语
    response = llm.invoke(f"用中文写一句友好的告别语，包含{state['name']}这个名字")
    print("Goodbye response:", response.content)  # 添加调试输出
    return {"bye": response.content}


# 2. 构建有向图（Graph），添加节点和边
from typing import TypedDict

class State(TypedDict):
    greet: str
    name: str
    bye: str

graph = StateGraph(state_schema=State)
graph.add_node("greet", greet)
graph.add_node("ask_name", ask_name)
graph.add_node("say_goodbye", say_goodbye)

# 设置入口节点
graph.set_entry_point("greet")  # 直接设置greet节点为入口点

# 添加边（定义节点之间的流转关系）
graph.add_edge("greet", "ask_name")
graph.add_edge("ask_name", "say_goodbye")
graph.add_edge("say_goodbye", END)  # END表示流程结束

# 3. 运行图（Graph）
app = graph.compile()
result = app.invoke({"name": "测试"})  # 提供一个包含name字段的输入
print("最终输出：", result)
