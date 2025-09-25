from langchain_openai import ChatOpenAI
from pydantic import SecretStr, BaseModel, Field
from langchain_core.tools import tool

from common.chat_prompt_template import chat_prompt_template

llm = ChatOpenAI(
    model="qwen-plus",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key=SecretStr("sk-d7f462f5a5d4447cad77ccffc6195a50"),
    streaming=True
)


class AddInputArgs(BaseModel):
    a: int = Field(description="first number")
    b: int = Field(description="second number")


@tool(
    description="add two number",
    args_schema=AddInputArgs
)
def add(a, b):
    return a + b


tool_dict_a = {
    "add": add,
}


def create_calc_tools():
    return [add]


llm_with_tools = llm.bind_tools(create_calc_tools())

chain = chat_prompt_template | llm_with_tools



