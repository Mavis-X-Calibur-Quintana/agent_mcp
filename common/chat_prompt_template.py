from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate


human_chat_message = HumanMessagePromptTemplate.from_template("用户问题:{question}")

system_chat_message = SystemMessagePromptTemplate.from_template("你是一位{role}专家，擅长回答{domain}领域的问题")

chat_prompt_template = ChatPromptTemplate.from_messages([
    system_chat_message,
    human_chat_message
])

chat_prompt = chat_prompt_template.format_messages(
    role="编程",
    domain="Web开发",
    question="如何构建一个基于Vue的前端应用"
)
