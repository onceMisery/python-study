"""
LangChain 基于知识库的问答系统基础示例

功能：
- 用RetrievalQA链实现多文档检索问答
- 适合Python初学者，包含详细注释

准备：
- 需先注册OpenAI账号，获取API Key
- 设置环境变量 OPENAI_API_KEY=你的key
- 安装依赖：pip install langchain openai tiktoken faiss-cpu
- 需准备 sample.txt 和 sample2.txt 作为知识库文档
"""

from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI

# 1. 加载多个本地文档
loader1 = TextLoader("06-langchain/sample.txt", encoding="utf-8")
loader2 = TextLoader("06-langchain/sample2.txt", encoding="utf-8")
docs1 = loader1.load()
docs2 = loader2.load()
all_docs = docs1 + docs2

# 2. 文本切分
text_splitter = CharacterTextSplitter(chunk_size=200, chunk_overlap=20)
split_docs = text_splitter.split_documents(all_docs)

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
question = "LangChain可以用来做什么？请简要说明。"
result = qa.run(question)
print("问题：", question)
print("知识库AI回答：", result) 