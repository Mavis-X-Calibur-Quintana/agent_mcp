import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import initialize_agent, AgentType
from langchain_core.prompts import PromptTemplate
from common.llm import llm, file_tools


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
        tools=tools + file_tools,
        llm=llm,
        agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True
    )

    prompt_template = PromptTemplate.from_template("你是一个智能助手，可以调用高德的 MCP 工具来解决问题。\n\n{input}")
    prompt = prompt_template.format_prompt(input="""
    目标:
    - 明天上午10点我要从北京南站到北京望京SOHO
    - 线路选择：公交地铁或打车
    - 考虑出行时间和路线，以及天气状况
    
    要求：
    - 制作网页来展示出行路线和位置,输出为html文件到E:\python\project\.temp目录下
    - 网页使用简约美观的页面风格，以及卡片展示
    - 行程规划的结果要能够在高德APP中显示，并集成到H5页面中
    """)

    return await agent.ainvoke(prompt)

asyncio.run(create_and_run_client())

# asyncio.run(create_amap_mcp_client())
