"""
LangGraph 复杂工作流基础示例

功能：
- 演示如何构建带分支、循环和多节点的智能工作流
- 适合Python初学者，包含详细注释

准备：
- 需先注册OpenAI账号，获取API Key
- 设置环境变量 OPENAI_API_KEY=你的key
- 安装依赖：pip install langgraph langchain openai
"""

from langgraph.graph import StateGraph, END

# 1. 定义节点函数
def start_node(state):
    print("节点1：开始流程")
    return {"step": 1, "count": state.get("count", 0)}

def process_node(state):
    count = state["count"] + 1
    print(f"节点2：处理步骤，当前计数={count}")
    return {"step": 2, "count": count}

def check_node(state):
    print(f"节点3：检查是否需要循环，当前计数={state['count']}")
    return state

def end_node(state):
    print("节点4：流程结束")
    return {"result": f"流程完成，总计数={state['count']}"}

# 2. 构建有向图，包含分支和循环
graph = StateGraph()
graph.add_node("start", start_node)
graph.add_node("process", process_node)
graph.add_node("check", check_node)
graph.add_node("end", end_node)

graph.add_edge("start", "process")
graph.add_edge("process", "check")
graph.add_edge("check", "process", condition=lambda state: state["count"] < 3)  # 循环条件

graph.add_edge("check", "end", condition=lambda state: state["count"] >= 3)
graph.add_edge("end", END)

# 3. 运行工作流
print("--- 运行复杂工作流 ---")
result = graph.invoke({"count": 0})
print("最终输出：", result) 