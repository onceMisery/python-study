# 智能客服机器人（LangChain + LangGraph 实战项目）

## 项目简介
本项目基于 LangChain 和 LangGraph，构建一个支持多轮对话、知识库问答、FAQ自动学习、工单流转的智能客服机器人。适合Python初学者和AI开发者学习与实践。

## 核心功能
- 多轮对话与上下文记忆
- FAQ/知识库检索（RAG）
- 工单创建与流转（模拟）
- 工具调用（如天气、快递查询等）
- 用户画像与个性化服务
- 流程分支与异常处理

## 目录结构
```
customer_service_bot/
  main.py              # 启动入口，集成所有流程
  graph.py             # LangGraph工作流定义
  tools.py             # 工具函数（如天气、快递、工单API等）
  memory.py            # 用户画像与上下文记忆管理
  knowledge_base.py    # FAQ与知识库检索
  data/
    faqs.txt           # FAQ知识库
    users.json         # 用户画像数据
  README.md            # 项目说明文档
```

## 环境准备
1. 推荐使用虚拟环境
2. 安装依赖：
   ```bash
   pip install langgraph langchain openai
   ```
3. 注册OpenAI账号，获取API Key
4. 设置环境变量：
   ```bash
   export OPENAI_API_KEY=你的key  # Windows下用 set OPENAI_API_KEY=你的key
   ```

## 运行方法
```bash
python main.py
```

## 多轮对话与上下文记忆
本项目支持多轮对话，机器人能记住上下文，连续理解和回答用户问题。
- 依赖LangChain的ConversationChain和Memory
- 运行后可多次输入，体验连续对话

## RAG知识库检索
本项目支持RAG（检索增强生成）智能问答：
- FAQ未命中时，自动进入知识库文档检索，结合大模型生成答案
- 支持在 data/docs/ 目录下添加更多知识库文档
- 依赖LangChain的文档加载、向量化、FAISS和RetrievalQA

## 外部API工具调用
本项目支持常用工具的自动调用：
- 天气查询：如“请查询北京的天气”
- 快递查询：如“帮我查一下快递1234567890的状态”
- 工具调用节点会自动识别意图并返回模拟结果（可扩展为真实API）

## 多Agent协作与分流
本项目支持多Agent协作：
- FAQAgent：负责FAQ知识库问答
- RAGAgent：负责知识库文档检索与智能问答
- ToolAgent：负责天气、快递等工具调用
- TicketAgent：负责工单创建
- 分流节点会根据用户问题类型自动分配给不同Agent处理，实现专家分工与协作

---

后续每个模块都配有详细注释和分步讲解，适合循序渐进学习和扩展。 