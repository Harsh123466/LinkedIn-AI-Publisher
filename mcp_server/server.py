from mcp.server import MCPServer
import os
from dotenv import load_dotenv
import requests
import sys


load_dotenv()


# create MCP server
mcp = MCPServer("LinkedIn MCP Server")

@mcp.tool()
def create_linkedin_post(content : str) -> str:
    """Create a LinkedIn post from the provided content."""

    print(f"CONTENT LENGTH: {len(content)}", file=sys.stderr)
    print(f"CONTENT RECEIVED:\n{content}", file=sys.stderr)

    # check for empty content
    if not content or not content.strip():
        return "ERROR: Post content cannot be empty."

    content = content.strip()

    if len(content) < 50:
        return "ERROR: Post is too short."

    access_token = os.getenv("LINKEDIN_ACCESS_TOKEN")
    member_id = os.getenv("LINKEDIN_MEMBER_ID")

    if not access_token:
        return "ERROR: LinkedIn access token is missing."

    if not member_id:
        return "ERROR: LinkedIn member ID is missing."

    author = f"urn:li:person:{member_id}"

    url = "https://api.linkedin.com/rest/posts"


    headers = {
        "Authorization": f"Bearer {access_token}",
        "X-Restli-Protocol-Version": "2.0.0",
        "Linkedin-Version": "202606",
        "Content-Type": "application/json"
    }

    payload = {
        "author": author,
        "commentary": content,
        "visibility": "PUBLIC",
        "distribution": {
            "feedDistribution": "MAIN_FEED",
            "targetEntities": [],
            "thirdPartyDistributionChannels": []
        },
        "lifecycleState": "PUBLISHED",
        "isReshareDisabledByAuthor": False
    }


    response = requests.post(
        url,
        headers=headers,
        json=payload
    )

    if response.status_code != 201:
        return f"ERROR: LinkedIn API failed: {response.text}"

    post_id = response.headers.get("x-restli-id")

    return f"LinkedIn post published successfully!\nPost ID: {post_id}"


if __name__ == "__main__":
    mcp.run()