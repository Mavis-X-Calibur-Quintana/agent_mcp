from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder


# 1. 创建一个MessagesPlaceholder作为模板的一部分，用于展示对话历史，其中chat_history变量用于存储上下文信息，确保多轮对话连贯性。
# 2. 设计模板以区分human和AI的发言，通过human message和AI message的格式填充，保证对话角色清晰。
# 3. 初始对话中chat_history为空，后续对话将填充此变量，实现对话历史的动态更新。
# 4. 在创建完prompt和model后，建立LCEL agent mult chart文件，用于定义链式调用关系，优化多轮对话流程。
# 5. 通过合理设计模板和链式调用关系，提升多轮对话系统的响应质量和用户体

multi_chat_prompt = ChatPromptTemplate([
    ("system","你是一位优秀的技术专家，擅长解决各种开发中的技术问题"),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human","{question}")
]
)