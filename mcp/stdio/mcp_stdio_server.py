from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Math tools")


@mcp.tool(description="add two number")
def add(a: int, b: int) -> int:
    return a + b


@mcp.tool(description="multiply two number")
def multiply(a: int, b: int) -> int:
    return a * b


if __name__ == "__main__":
    mcp.run(transport="stdio")
