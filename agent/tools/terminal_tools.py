from agent.utils.mcp import create_mcp_stdio_client


async def get_stdio_terminal_tools():
    params = {
        "command": "python",
        "args": [
            "E:\python\project\agent\mcp\terminal_tools.py",
        ]
    }

    client, tools = await create_mcp_stdio_client("terminal_tools", params)

    return tools
