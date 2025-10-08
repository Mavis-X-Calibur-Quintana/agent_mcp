import os
from langchain_community.embeddings import DashScopeEmbeddings
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_chroma import Chroma

os.environ["DASHSCOPE_API_KEY"] = "sk-d7f462f5a5d4447cad77ccffc6195a50"

# 实例化文档加载器
loader = TextLoader("./state_of_the_union.txt",encoding="utf-8")
# 加载文档
documents = loader.load()
# print(documents)

# 实例化文本分割器
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
# 分割文本
docs = text_splitter.split_documents(documents)
# print(docs)

# 构建Embedding模型
embeddings = DashScopeEmbeddings()
# Chroma 向量数据库，使用 docs 的向量作为初始化存储, 并持久化存储
db = Chroma.from_documents(docs, embeddings,persist_directory="./chroma_db")
# 构造提问 query
query = "What did the president say about Ketanji Brown Jackson"
# 在 Chroma 中进行相似度搜索，找出与 query 最相似结果
docs = db.similarity_search(query)
# 输出 Chroma 中最相似结果
print(docs[0].page_content)

