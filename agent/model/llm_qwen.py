from langchain_openai import ChatOpenAI
from pydantic import SecretStr

llm_qwen = ChatOpenAI(
    model="qwen3-max",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key=SecretStr("sk-d7f462f5a5d4447cad77ccffc6195a50"),
    streaming=True
)




