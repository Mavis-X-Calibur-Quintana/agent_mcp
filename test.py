from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import SecretStr

llm = ChatOpenAI(
    model="qwen-plus",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key=SecretStr("sk-d7f462f5a5d4447cad77ccffc6195a50"),
    streaming=True
)


prompt_template = FewShotPromptTemplate(
    examples=[
        {"input": "hello", "output": "你好！"},
        {"input": "today", "output": "今天！"},
        {"input": "goodbye", "output": "再见！"},
    ],
    example_prompt=PromptTemplate.from_template("输入：{input}\n输出：{output}"),
    prefix="以下是一些输入-输出对的示例：",
    suffix="输入：{input}\n输出：",
    input_variables=["input"],
)


prompt = prompt_template.format(input="beautiful")


result = llm.invoke(prompt)
print(result.content)


