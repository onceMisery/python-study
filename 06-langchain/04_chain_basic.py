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
import os

from dotenv import load_dotenv
from langchain.chains import LLMChain  # 修复：导入缺失的 LLMChain 模块
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

# 定义一个带变量的提示模板
prompt_template = ChatPromptTemplate([("system", "You are a helpful assistant"),
                                      ("user", "Tell me a joke about {topic}")])

load_dotenv()
print(prompt_template.invoke({"topic": "cats"}))
# 初始化 DeepSeek LLM
llm = ChatOpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),  # 使用环境变量获取 API Key
    base_url="https://api.deepseek.com",
    temperature=0.7,
    model="deepseek-chat"  # 指定模型名称（可选）
)

# 创建LLMChain，将PromptTemplate和LLM串联
chain = prompt_template | llm

# 运行链式调用，传入变量
result = chain.invoke({"topic": "Python"})

print("AI回答：", result)
