import asyncio

from mcp import ClientSession, StdioServerParameters, stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from common.llm import llm
from langchain.agents import initialize_agent, AgentType


async def create_playwright_stdio_client():
    # server_params = StdioServerParameters(
    #     command="npx",
    #     args=["@playwright/mcp@latest", "--headless"]
    # )

    server_params = StdioServerParameters(
        command="npx",
        args=["@playwright/mcp@latest", "--headless"]
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools = await load_mcp_tools(session)
            print(tools)

            agent = create_react_agent(
                tools=tools,
                model=llm,
                debug=True
            )

            resp = await agent.ainvoke(input={"messages": [{"role": "user", "content": "在百度中查询北京今天的天气"}]})
            print(resp)


asyncio.run(create_playwright_stdio_client())
