"""
RAG知识库检索模块
- 基于LangChain文档加载、向量化、FAISS和RetrievalQA
- 适合Python初学者
"""
import os
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI

# 加载知识库文档并构建向量数据库
def build_vectorstore():
    docs_dir = os.path.join(os.path.dirname(__file__), 'data', 'docs')
    all_docs = []
    for fname in os.listdir(docs_dir):
        if fname.endswith('.txt') or fname.endswith('.md'):
            loader = TextLoader(os.path.join(docs_dir, fname), encoding='utf-8')
            all_docs.extend(loader.load())
    splitter = CharacterTextSplitter(chunk_size=300, chunk_overlap=30)
    split_docs = splitter.split_documents(all_docs)
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(split_docs, embeddings)
    return vectorstore

# 检索问答接口
def rag_qa(question, vectorstore=None):
    if vectorstore is None:
        vectorstore = build_vectorstore()
    qa = RetrievalQA.from_chain_type(
        llm=OpenAI(temperature=0),
        chain_type="stuff",
        retriever=vectorstore.as_retriever()
    )
    return qa.run(question) 