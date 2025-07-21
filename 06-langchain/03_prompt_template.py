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
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
import os

load_dotenv()
# 定义一个带变量的提示模板
prompt = PromptTemplate(
    input_variables=["language"],
    template="请用一句话介绍一下{language}语言的主要特点。"
)

# 渲染模板，生成具体的提示内容
prompt_text = prompt.format(language="Python")

# 初始化 DeepSeek LLM
llm = ChatOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),  # 使用环境变量获取 API Key
    base_url="https://api.deepseek.com",
    temperature=0.7,
    model="deepseek-chat"  # 指定模型名称（可选）
)

# 用渲染后的提示进行问答
answer = llm.invoke([{"role": "user", "content": prompt_text}])

print("问题：", prompt_text)
print("回答：", answer.content)