import asyncio

from mcp import StdioServerParameters, ClientSession
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain.agents import initialize_agent, AgentType
from common.llm import llm


async def create_map_stdio_client():
    server_params = StdioServerParameters(
        command="python",
        args=["E:\python\project\mcp\stdio\mcp_stdio_server.py"]
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await load_mcp_tools(session)
            print(tools)

            agent = initialize_agent(
                tools=tools,
                llm=llm,
                agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
                verbose=True
            )

            resp = await agent.ainvoke("1 + 5 * 488 = ?")
            print(resp)


asyncio.run(create_map_stdio_client())
