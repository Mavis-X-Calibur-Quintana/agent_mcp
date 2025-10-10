from langchain_core.runnables import RunnableConfig
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from langchain.agents.agent_toolkits.file_management.toolkit import FileManagementToolkit
from langgraph.checkpoint.redis import RedisSaver
from langgraph.checkpoint.mongodb import MongoDBSaver
from agent.model.llm_qwen import llm_qwen


def create_agent():
    file_tools = FileManagementToolkit(root_dir="E:\\AI\\agent_mcp\\agent\\.temp").get_tools()

    # with RedisSaver.from_conn_string("redis://localhost:6379") as memory:

    MONGODB_URI = "mongodb://root:root@127.0.0.1:27017"
    MONGODB_DB = "chat"

    with MongoDBSaver.from_conn_string(MONGODB_URI, MONGODB_DB) as memory:

        agent = create_react_agent(
            tools=file_tools,
            model=llm_qwen,
            checkpointer=memory,
            debug=True
        )

        config = RunnableConfig(configurable={"thread_id": 5})

        # res = agent.invoke(input={"messages": [("user", "我叫Sam")]}, config=config)
        res = agent.invoke(input={"messages": [("user", "我是谁？")]}, config=config)
        # res = agent.invoke(input={"messages": [("user", "我们刚才聊了什么？")]}, config=config)
        print("=" * 60)
        print(res)
        print("=" * 60)
        memory.close()


if __name__ == '__main__':
    create_agent()
