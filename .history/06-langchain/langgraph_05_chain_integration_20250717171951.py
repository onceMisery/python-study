"""
LangGraph 与 LangChain 结合基础示例

功能：
- 演示如何在LangGraph节点中集成LangChain的LLMChain，实现复杂对话或问答
- 适合Python初学者，包含详细注释

准备：
- 需先注册OpenAI账号，获取API Key
- 设置环境变量 OPENAI_API_KEY=你的key
- 安装依赖：pip install langgraph langchain openai
"""

from langgraph.graph import StateGraph, END
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# 1. 定义集成LangChain LLMChain的节点
def ask_python_vs_java(state):
    llm = OpenAI(temperature=0)
    prompt = PromptTemplate(
        input_variables=["lang1", "lang2"],
        template="请简要对比一下{lang1}和{lang2}的主要区别。"
    )
    chain = LLMChain(llm=llm, prompt=prompt)
    lang1 = state.get("lang1", "Python")
    lang2 = state.get("lang2", "Java")
    print(f"节点：调用LLMChain对比{lang1}和{lang2}")
    answer = chain.run({"lang1": lang1, "lang2": lang2})
    return {"compare_answer": answer}

# 2. 定义结束节点
def end_node(state):
    print("流程结束，输出对比结果")
    return {"final": state["compare_answer"]}

# 3. 构建有向图，集成LLMChain
graph = StateGraph()
graph.add_node("compare", ask_python_vs_java)
graph.add_node("end", end_node)

graph.add_edge("compare", "end")
graph.add_edge("end", END)

# 4. 运行图
init_state = {"lang1": "Python", "lang2": "Java"}
result = graph.invoke(init_state)
print("最终输出：", result) 