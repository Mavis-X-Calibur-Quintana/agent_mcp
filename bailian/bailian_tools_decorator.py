from common.chat_prompt_template import chat_prompt_template
from common.llm import llm
from langchain_core.tools import tool
from pydantic import BaseModel, Field


class AddInputArgs(BaseModel):
    a: str = Field(description="first number")
    b: str = Field(description="second number")


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

resp = chain.invoke(input={"role": "计算", "domain": "数学计算", "question": "100+100=?"})
print(resp)

for tool_calls in resp.tool_calls:
    print(tool_calls)
    args = tool_calls["args"]
    print(args)
    func_name = tool_calls["name"]
    print(func_name)

    tool_func = tool_dict_a[func_name]
    tool_content = tool_func.invoke(args)
    print(tool_content)
