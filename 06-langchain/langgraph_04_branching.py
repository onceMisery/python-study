"""
LangGraph 状态管理与分支基础示例

功能：
- 演示如何根据状态条件实现流程分支（if/else逻辑）
- 适合Python初学者，包含详细注释

准备：
- 需先注册OpenAI账号，获取API Key
- 设置环境变量 OPENAI_API_KEY=你的key
- 安装依赖：pip install langgraph langchain openai
"""

from langgraph.graph import StateGraph, END

# 1. 定义节点函数
def check_score(state):
    score = state.get("score", 0)
    print(f"节点1：检查分数，当前分数={score}")
    return {"score": score}

def pass_node(state):
    print("节点2：分支-及格")
    return {"result": "恭喜你，及格了！"}

def fail_node(state):
    print("节点3：分支-不及格")
    return {"result": "很遗憾，未及格。"}

# 2. 构建有向图，添加分支逻辑
graph = StateGraph()
graph.add_node("check", check_score)
graph.add_node("pass", pass_node)
graph.add_node("fail", fail_node)

graph.add_edge("check", "pass", condition=lambda state: state["score"] >= 60)
graph.add_edge("check", "fail", condition=lambda state: state["score"] < 60)
graph.add_edge("pass", END)
graph.add_edge("fail", END)

# 3. 运行图，测试不同分数
print("--- 测试及格分支 ---")
result1 = graph.invoke({"score": 85})
print("最终输出：", result1)

print("\n--- 测试不及格分支 ---")
result2 = graph.invoke({"score": 45})
print("最终输出：", result2) 