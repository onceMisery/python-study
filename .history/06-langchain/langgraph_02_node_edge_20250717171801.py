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

from langgraph.graph import StateGraph, END

# 1. 定义节点函数（每个节点就是一个Python函数）
def greet(state):
    print("节点1：问候用户")
    return {"greet": "你好，欢迎使用LangGraph！"}

def ask_name(state):
    print("节点2：询问用户姓名")
    # 这里模拟输入，实际可用input()或集成LLM
    return {"name": "小明"}

def say_goodbye(state):
    print("节点3：结束对话")
    return {"bye": f"再见，{state['name']}！"}

# 2. 构建有向图（Graph），添加节点和边
graph = StateGraph()
graph.add_node("greet", greet)
graph.add_node("ask_name", ask_name)
graph.add_node("say_goodbye", say_goodbye)

# 添加边（定义节点之间的流转关系）
graph.add_edge("greet", "ask_name")
graph.add_edge("ask_name", "say_goodbye")
graph.add_edge("say_goodbye", END)  # END表示流程结束

# 3. 运行图（Graph）
result = graph.invoke({})
print("最终输出：", result) 