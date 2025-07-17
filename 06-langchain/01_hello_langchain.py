"""
第一个LangChain程序：Hello, LLM!

功能：
- 用LangChain调用OpenAI大模型，完成一次最基础的问答。
- 适合Python初学者，包含详细注释。

准备：
- 需先注册OpenAI账号，获取API Key。
- 设置环境变量 OPENAI_API_KEY=你的key
- 安装依赖：pip install langchain openai
"""

from langchain.llms import OpenAI

# 初始化OpenAI LLM（需设置OPENAI_API_KEY环境变量）
llm = OpenAI(temperature=0.7)

# 发送一个简单的提问
question = "用一句话介绍一下LangChain是什么？"
answer = llm(question)

print("问题：", question)
print("回答：", answer) 