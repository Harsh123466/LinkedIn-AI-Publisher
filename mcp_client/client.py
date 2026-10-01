import asyncio
from mcp import Client, StdioServerParameters


async def send_post_to_mcp(content: str):

    # Tell the MCP client how to start our server
    server_params = StdioServerParameters(
        command="python",
        args=["mcp_server/server.py"]
    )

    # Connect to the MCP server
    async with Client(server_params) as client:

        print("Connected to MCP server!")

        # Discover available tools
        tools = await client.list_tools()

        print("\n Available tools:")

        for tool in tools.tools:
            print(f"-{tool.name}")

        # Calls MCP tool
        result = await client.call_tool(
            "create_linkedin_post",
            {
                "content": content
            }
        )

        return result


if __name__ == "__main__":
    result = asyncio.run(
    send_post_to_mcp(
        """AI agents are changing software development by moving beyond simple code completion. 
        Developers can now use agents to plan tasks, write code, run tests, analyze failures, and improve their solutions automatically. 
        This changes the developer's role from writing every line manually to designing reliable workflows and giving AI the right context and tools."""
            )
        )

    print("\nTool result:")
    print(result)
