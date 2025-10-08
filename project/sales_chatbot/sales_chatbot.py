import gradio as gr
import os
from langchain_community.embeddings import DashScopeEmbeddings
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI
from langchain_chroma import Chroma
from pydantic import SecretStr

os.environ["DASHSCOPE_API_KEY"] = "sk-d7f462f5a5d4447cad77ccffc6195a50"

def initialize_sales_bot(vector_store_dir: str = "db"):
    db = Chroma(persist_directory=vector_store_dir, embedding_function=DashScopeEmbeddings())
    llm = ChatOpenAI(
        model="qwen3-max",
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        api_key=SecretStr("sk-d7f462f5a5d4447cad77ccffc6195a50"),
        streaming=True
    )

    global SALES_BOT
    SALES_BOT = RetrievalQA.from_chain_type(llm,
                                            retriever=db.as_retriever(search_type="similarity_score_threshold",
                                                                      search_kwargs={"score_threshold": 0.8}))
    # 返回向量数据库的检索结果
    SALES_BOT.return_source_documents = True

    return SALES_BOT


def sales_chat(message, history):
    print(f"[message]{message}")
    print(f"[history]{history}")
    # TODO: 从命令行参数中获取
    enable_chat = True

    ans = SALES_BOT({"query": message})
    # 如果检索出结果，或者开了大模型聊天模式
    # 返回 RetrievalQA combine_documents_chain 整合的结果
    if ans["source_documents"] or enable_chat:
        print(f"[result]{ans['result']}")
        print(f"[source_documents]{ans['source_documents']}")
        return ans["result"]
    # 否则输出套路话术
    else:
        return "这个问题我要问问领导"


def launch_gradio():
    demo = gr.ChatInterface(
        fn=sales_chat,
        title="房产销售",
        # retry_btn=None,
        # undo_btn=None,
        chatbot=gr.Chatbot(height=600),
    )

    demo.launch(share=True, server_name="0.0.0.0")


if __name__ == "__main__":
    # 初始化房产销售机器人
    initialize_sales_bot()
    # 启动 Gradio 服务
    launch_gradio()
