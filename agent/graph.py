import os
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import ToolNode
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv
import time
from langchain_core.messages import ToolMessage
from agent.tools import tool
from agent.prompt import WRITER_SYSTEM_PROMPT, REVIEWER_SYSTEM_PROMPT
from agent.state import State


load_dotenv()


# llms

# for write
# writer_llm = ChatGoogleGenerativeAI(
#     model="gemini-3-flash-preview",
#     temperature=0.7
# )

writer_llm = ChatGroq(
    model="qwen/qwen3.8-27b",
    temperature=0.7
)

writer_llm_with_tools = writer_llm.bind_tools(tool)

# for reviewer
reviewer_llm = ChatGroq(
    model="qwen/qwen3.8-27b",
    temperature=0.2
)


def writer_node(state: State) -> dict:
    """Generate or rewrite the LinkedIn post."""

    topic = state["topic"]
    previous_feedback = state["review_feedback"]

    # Check whether we are continuing after a tool call
    messages = state["messages"]

    # If there are existing messages and the last message is a tool result,
    # continue the same conversation.
    if messages and isinstance(messages[-1], ToolMessage):

        start = time.time()

        response = writer_llm_with_tools.invoke(
            [
                ("system", WRITER_SYSTEM_PROMPT),
                *messages
            ]
        )

        print(f"Writer took {time.time() - start:.2f} seconds")
        # print("TOOL CALLS:", response.tool_calls)

        return {
            "messages": [response]
        }

    # Otherwise, this is a NEW draft attempt
    attempt = state.get("attempt", 0) + 1

    if attempt == 1:
        user_message = (
            f"Write a LinkedIn post on this topic: {topic}\n\n"
            "If current information is required, use the web search tool."
        )
    else:
        user_message = (
            f"Your previous draft on '{topic}' was rejected.\n\n"
            f"Reviewer's feedback:\n{previous_feedback}\n\n"
            "Write a completely improved version that fixes every issue "
            "mentioned in the feedback."
        )

    start = time.time()

    response = writer_llm_with_tools.invoke(
        [
            ("system", WRITER_SYSTEM_PROMPT),
            ("human", user_message)
        ]
    )

    print(f"Writer took {time.time() - start:.2f} seconds")
    # print("TOOL CALLS:", response.tool_calls)

    return {
        "messages": [
            ("human", user_message),
            response
        ],
        "attempt": attempt
    }


tool_node = ToolNode(tool)


def extract_draft_node(state : State) -> dict:
    """After the writer finishes tool calls, pulls the final text out as the draft."""
    last_message = state['messages'][-1]
    draft = last_message.content
    print(f"\n\n generated post \n {draft} \n ")
    return {"draft" : draft}



def reviewer_node(state : State) -> dict:
    """Reviews the draft and decides: approve or reject with feedback."""

    draft = state['draft']

    prompt = (
        f"review this LinkedIn post draft : \n"
        f"{draft}\n"
        f"give your reviews"
    )

    start = time.time()

    response = reviewer_llm.invoke(
        [("system",REVIEWER_SYSTEM_PROMPT), ("human",prompt)]
    )

    print(f"Writer took {time.time() - start:.2f} seconds")

    review_text = response.content.strip()

    is_approved = "APPROVED" in review_text.upper().split("FEEDBACK")[0]

    if "FEEDBACK:" in review_text:
        feedback = review_text.split("FEEDBACK:", 1)[1].strip()
    else:
        feedback = review_text

    verdict = "APPROVED" if is_approved else "REJECTED"
    print(f"[Verdict: {verdict}]")
    print(f"[Feedback: {feedback}]")

    return {
        "review_feedback": feedback,
        "is_approved": is_approved,
    }


# router func for iterations

def should_use_tool(state : State):
    last_message = state['messages'][-1]

    if getattr(last_message, 'tool_calls', None):
        return "tools"
    return "extract_draft"

def should_stop_looping(state:State):
    if state['is_approved']:
        print('Post has been approved')
        return END
    if state['attempt'] >= 5:
        print('reached max attempts')
        return END
    return 'writer'


# build the graph

graph = StateGraph(State)

graph.add_node('writer',writer_node)
graph.add_node('tools',tool_node)
graph.add_node('extract_draft',extract_draft_node)
graph.add_node('reviewer',reviewer_node)


graph.add_edge(START, 'writer')

graph.add_conditional_edges(
    'writer' , should_use_tool
)

graph.add_edge('tools','writer')
graph.add_edge('extract_draft','reviewer')

graph.add_conditional_edges(
    'reviewer', should_stop_looping
)
 
app = graph.compile()



# if __name__ == "__main__":

#     print("=" * 55)
#     print("Welcome to the LinkedIn Post Generator")
#     print("=" * 55)

#     print("\nThis tool will draft a LinkedIn post for you, review it")
#     print("itself, and iterate until it's publish-ready.")

#     print("=" * 55)

#     topic = input("\nWhat topic do you want a LinkedIn post about?\n> ").strip()

#     if not topic:
#         print("\nNo topic given. Exiting.")
#     else:
#         print("\nStarting generation...\n")

#         initial_state = {
#             "topic": topic,
#             "messages": [],
#             "draft": "",
#             "review_feedback": "",
#             "is_approved": False,
#             "attempt": 0,
#         }

#         final_state = app.invoke(initial_state)

#         print("\n" + "=" * 55)
#         print("FINAL LINKEDIN POST")
#         print("=" * 55)
#         print(final_state["draft"])
#         print("=" * 55)
#         print(f"Total attempts: {final_state['attempt']}")
#         print(f"Approved: {final_state['is_approved']}")