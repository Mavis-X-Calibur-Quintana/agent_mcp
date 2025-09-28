import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import initialize_agent, AgentType
from langchain_core.prompts import PromptTemplate
from common.llm import llm


async def create_amap_mcp_client():
    mcp_config = {
        "amap": {
            "url": "https://mcp.amap.com/sse?key=3b8d4c1df04b76185896ef09d1927266",
            "transport": "sse"   # 指定使用sse传输
        }
    }
    client = MultiServerMCPClient(mcp_config)
    print(client)

    tools = await client.get_tools()
    print(tools)

    return client, tools


async def create_and_run_client():
    client, tools = await create_amap_mcp_client()
    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True
    )

    prompt_template = PromptTemplate.from_template("你是一个智能助手，可以调用高德的 MCP 工具来解决问题。\n\n{input}")
    prompt = prompt_template.format_prompt(input="查询北京天安门的地理位置")

    return await agent.ainvoke(prompt)

asyncio.run(create_and_run_client())

# asyncio.run(create_amap_mcp_client())
