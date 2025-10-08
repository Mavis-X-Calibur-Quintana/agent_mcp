import os
from langchain_community.utilities import SerpAPIWrapper
from langchain.agents import Tool
from langchain_community.tools import WriteFileTool, ReadFileTool
# from langchain_openai import OpenAIEmbeddings  必须使用openai的api key
from langchain_community.embeddings import DashScopeEmbeddings  
from langchain_chroma import Chroma
from langchain_experimental.autonomous_agents import AutoGPT
from langchain_openai import ChatOpenAI
from pydantic import SecretStr


os.environ["SERPAPI_API_KEY"] = "696a327c9dd33594732dcfcb13f5618d62ad9e13555c58600d624c05d8ed67b8"
os.environ["DASHSCOPE_API_KEY"] = "sk-d7f462f5a5d4447cad77ccffc6195a50"
# 构造 AutoGPT 的工具集
search = SerpAPIWrapper()
tools = [
    Tool(
        name="search",
        func=search.run,
        description="useful for when you need to answer questions about current events. You should ask targeted questions",
    ),
    WriteFileTool(),
    ReadFileTool(),
]
# DashScopeEmbeddings 模型(兼容国产大模型)
embeddings_model = DashScopeEmbeddings()
# 实例化 Chroma 向量数据库
vectorstore = Chroma(
    embedding_function=embeddings_model,
    persist_directory="./chroma_db"  # 持久化存储目录
)
agent = AutoGPT.from_llm_and_tools(
    ai_name="Jarvis",
    ai_role="Assistant",
    tools=tools,
    llm=ChatOpenAI(
        model="qwen3-max",
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        api_key=SecretStr("sk-d7f462f5a5d4447cad77ccffc6195a50"),
        streaming=True
    ),
    memory=vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 4}  # 返回最相似的4个文档
    ),
)

# 打印 Auto-GPT 内部的 chain 日志
agent.chain.verbose = True

agent.run(["2023年成都大运会，中国金牌数是多少"])
