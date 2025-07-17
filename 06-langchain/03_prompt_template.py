"""
LangChain 提示模板（PromptTemplate）基础示例

功能：
- 用PromptTemplate灵活构建复杂提示，提升模型输出质量
- 支持变量替换，适合批量生成和动态问答
- 适合Python初学者，包含详细注释

准备：
- 需先注册OpenAI账号，获取API Key
- 设置环境变量 OPENAI_API_KEY=你的key
- 安装依赖：pip install langchain openai
"""

from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI

# 定义一个带变量的提示模板
prompt = PromptTemplate(
    input_variables=["language"],
    template="请用一句话介绍一下{language}语言的主要特点。"
)

# 渲染模板，生成具体的提示内容
prompt_text = prompt.format(language="Python")

# 初始化OpenAI LLM
llm = OpenAI(temperature=0.7)

# 用渲染后的提示进行问答
answer = llm(prompt_text)

print("问题：", prompt_text)
print("回答：", answer) 