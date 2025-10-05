import uuid
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import PromptTemplate
from agent.model.llm_qwen import llm_qwen
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableWithMessageHistory
from agent.prompts.multi_chat_prompt import multi_chat_prompt
from langchain_community.chat_message_histories import FileChatMessageHistory
from langchain_community.agent_toolkits.file_management import FileManagementToolkit

file_tools = FileManagementToolkit(root_dir="E:\\AI\\agent_mcp\\agent\\.temp").get_tools()

llm_with_tools = llm_qwen.bind_tools(tools=file_tools)
chain = multi_chat_prompt | llm_with_tools | StrOutputParser()

def get_session_history(session_id:str):
    return FileChatMessageHistory(f'{session_id}.json')

chat_with_history = RunnableWithMessageHistory(
    runnable=chain,
    get_session_history=get_session_history,
    input_messages_key="question",
    history_messages_key="chat_history",
)

# chat_session_id = uuid.uuid4()
chat_session_id = "1"

# print(chat_session_id)

while True:
    user_input = input("用户: ")
    if user_input.lower() == "exit" or user_input.lower() == "quit":
        break

    response = chat_with_history.invoke(
        {"question": user_input},
        config={"configurable": {"session_id":chat_session_id}},
    )

    print("助理: ")
    for chunk in response:
        print(chunk,end="")
