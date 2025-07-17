"""
LangChain 链式调用（Chain）基础示例

功能：
- 用LLMChain将PromptTemplate和LLM串联，形成可复用的AI流程
- 适合Python初学者，包含详细注释

准备：
- 需先注册OpenAI账号，获取API Key
- 设置环境变量 OPENAI_API_KEY=你的key
- 安装依赖：pip install langchain openai
"""

from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.chains import LLMChain

# 定义一个带变量的提示模板
prompt = PromptTemplate(
    input_variables=["language"],
    template="请用一句话介绍一下{language}语言的主要特点。"
)

# 初始化OpenAI LLM
llm = OpenAI(temperature=0.7)

# 创建LLMChain，将PromptTemplate和LLM串联
chain = LLMChain(llm=llm, prompt=prompt)

# 运行链式调用，传入变量
result = chain.run({"language": "Python"})

print("AI回答：", result) 