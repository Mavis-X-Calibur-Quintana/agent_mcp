from agent.utils.mcp import create_mcp_stdio_client


async def get_stdio_powershell_tools():
    params = {
        "command": "python",
        "args": [
            "E:\python\project\agent\mcp\powershell_tools.py",
        ]
    }

    client, tools = await create_mcp_stdio_client("owershell_tools", params)

    return tools
