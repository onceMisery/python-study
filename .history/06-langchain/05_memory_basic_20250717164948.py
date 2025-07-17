"""
LangChain 记忆（Memory）机制基础示例

功能：
- 用ConversationBufferMemory让AI记住对话历史，实现多轮上下文对话
- 适合Python初学者，包含详细注释

准备：
- 需先注册OpenAI账号，获取API Key
- 设置环境变量 OPENAI_API_KEY=你的key
- 安装依赖：pip install langchain openai
"""

from langchain.memory import ConversationBufferMemory
from langchain.llms import OpenAI
from langchain.chains import ConversationChain

# 初始化OpenAI LLM
llm = OpenAI(temperature=0.7)

# 创建对话记忆对象
memory = ConversationBufferMemory()

# 创建ConversationChain，集成记忆机制
conversation = ConversationChain(
    llm=llm,
    memory=memory,
    verbose=True  # 输出详细对话过程，便于学习
)

# 多轮对话示例
print(conversation.predict(input="你好，请介绍一下LangChain。"))
print(conversation.predict(input="它和直接用OpenAI API有什么区别？"))
print(conversation.predict(input="能用一句话总结一下吗？")) 