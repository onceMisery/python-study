"""
LangChain RAG（检索增强生成）基础示例

功能：
- 加载本地文档，进行向量化和相似度检索
- 结合大模型实现“带知识库”的智能问答
- 适合Python初学者，包含详细注释

准备：
- 需先注册OpenAI账号，获取API Key
- 设置环境变量 OPENAI_API_KEY=你的key
- 安装依赖：pip install langchain openai tiktoken faiss-cpu
- 需准备 sample.txt 作为知识库文档
"""

from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI

# 1. 加载本地文档
loader = TextLoader("06-langchain/sample.txt", encoding="utf-8")
docs = loader.load()

# 2. 文本切分（长文档分段）
text_splitter = CharacterTextSplitter(chunk_size=200, chunk_overlap=20)
split_docs = text_splitter.split_documents(docs)

# 3. 文档向量化并存入向量数据库
embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_documents(split_docs, embeddings)

# 4. 构建带检索的问答链
qa = RetrievalQA.from_chain_type(
    llm=OpenAI(temperature=0),
    chain_type="stuff",
    retriever=vectorstore.as_retriever()
)

# 5. 进行知识库问答
question = "请用中文简要介绍LangChain的核心功能。"
result = qa.run(question)
print("问题：", question)
print("知识库AI回答：", result) 