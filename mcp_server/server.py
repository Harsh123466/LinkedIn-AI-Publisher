from mcp.server import MCPServer

# create MCP server
mcp = MCPServer("LinkedIn MCP Server")

@mcp.tool()
def create_linkedin_post(content : str) -> str:
    """Create a LinkedIn post from the provided content."""

    # check for empty content
    if not content or not content.strip():
        return "ERROR: Post content cannot be empty."

    content = content.strip()

    if len(content) < 50:
        return "ERROR: Post is too short."

    return f"LinkedIn post created successfully:\n\n{content}"

if __name__ == "__main__":
    mcp.run()