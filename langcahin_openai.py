from langchain_openai import ChatOpenAI
from pydantic import SecretStr
from langchain_core.prompts import HumanMessagePromptTemplate,SystemMessagePromptTemplate,ChatPromptTemplate

llm = ChatOpenAI(
    model="qwen-plus",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key=SecretStr("sk-d7f462f5a5d4447cad77ccffc6195a50"),
    streaming=True
)

human_chat_message = HumanMessagePromptTemplate.from_template("用户问题:{question}")

system_chat_message = SystemMessagePromptTemplate.from_template("你是一位{role}专家，擅长回答{domain}领域的问题")

prompt_template = ChatPromptTemplate.from_messages([
    system_chat_message,
    human_chat_message
])

prompt = prompt_template.format_messages(
    role="编程",
    domain="Web开发",
    question="如何构建一个基于Vue的前端应用"
)
# resp = llm.invoke(
#     "你好",
#     stop=["\n\n"],
# )
# print(resp.content)

resp = llm.stream(prompt)
for chunk in resp:
    print(chunk.content, end="")
