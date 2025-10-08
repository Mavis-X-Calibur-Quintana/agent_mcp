import os
from typing import List

from langchain.text_splitter import CharacterTextSplitter
from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings


os.environ["DASHSCOPE_API_KEY"] = "sk-d7f462f5a5d4447cad77ccffc6195a50"

with open("real_estate_sales_data.txt",encoding="utf-8") as f:
    real_estate_sales = f.read()


text_splitter = CharacterTextSplitter(
    separator = r'\d+\.',
    chunk_size = 100,
    chunk_overlap  = 0,
    length_function = len,
    is_separator_regex = True,
)

docs = text_splitter.create_documents([real_estate_sales])
db = Chroma.from_documents(docs, DashScopeEmbeddings(),persist_directory="./db")

# query = "小区吵不吵"
# # answer_list = db.similarity_search(query)
# # for ans in answer_list:
# #     print(ans.page_content + "\n")
#
# # 实例化一个 TopK Retriever
# topK_retriever = db.as_retriever(search_kwargs={"k": 3})
#
# # docs = topK_retriever.invoke(query)
# # for doc in docs:
# #     print(doc.page_content + "\n")
# #
# # docs = topK_retriever.invoke("你们有没有1000万的豪宅啊？")
# # for doc in docs:
# #     print(doc.page_content + "\n")
#
# # 实例化一个 similarity_score_threshold Retriever
# retriever = db.as_retriever(
#     search_type="similarity_score_threshold",
#     search_kwargs={"score_threshold": 0.8}
# )
#
# docs = topK_retriever.invoke(query)
# # for doc in docs:
# #     print(doc.page_content + "\n")
#
# ans = docs[0].page_content.split("[销售回答] ")[-1]
# print(ans)

def sales(query: str, score_threshold: float=0.8) -> List[str]:
    retriever = db.as_retriever(search_type="similarity_score_threshold", search_kwargs={"score_threshold": score_threshold})
    docs_list = retriever.invoke(query)
    ans_list = [doc.page_content.split("[销售回答] ")[-1] for doc in docs_list]

    return ans_list

print(sales("我想离医院近点", score_threshold=0.8))