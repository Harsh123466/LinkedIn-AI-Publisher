from agent.graph import app
from mcp_client.client import send_post_to_mcp
import asyncio 

topic = input("Topic: ")


initial_state = {
    "topic": topic,
    "messages": [],
    "draft": "",
    "review_feedback": "",
    "is_approved": False,
    "attempt": 0,
}

final_state = app.invoke(initial_state)
draft = final_state.get("draft", "").strip()

if not draft:
    print("\nFailed to generate the LinkedIn post.")
    print("Please try again with a different topic.")
    exit()



print("\n Generated LinkedIn post:")
print(draft)


choice = input("\nDo you want to publish this post? (y/n): ").strip().lower()

if choice == "y":
    result = asyncio.run(
        send_post_to_mcp(final_state["draft"])
    )

    print("\nMCP Result:")
    print(result)

    if "ERROR:" in str(result):
        print("\n❌ Post was not published.")
    else:
        print("\n✅ Post was accepted by MCP.")

else:
    print("\nPost was not published.")