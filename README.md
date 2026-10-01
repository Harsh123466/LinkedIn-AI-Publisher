# 🚀 AI LinkedIn Post Generator using MCP

An AI-powered LinkedIn Post Generator that automatically *** generates a LinkedIn post, reviews it, asks for human approval, and publishes it to LinkedIn using Model Context Protocol (MCP).**

This project was built to understand how **MCP can connect an AI application with external services through tools**.

---

## 📌 What is this project?

Normally, an AI application that wants to publish something on LinkedIn needs to directly integrate with the LinkedIn API.

In this project, I used **MCP (Model Context Protocol)** as the communication layer between my AI application and LinkedIn.

The AI application does not directly call the LinkedIn API.

Instead:

```text
AI Application
      ↓
   MCP Client
      ↓
   MCP Server
      ↓
 LinkedIn API
      ↓
   LinkedIn
```

The MCP server exposes a tool:

```text
create_linkedin_post
```

The AI application calls this MCP tool when the user approves the generated post.

---

# ✨ Features

* 🤖 AI-powered LinkedIn post generation
* 🔎 Web research using Tavily
* 📝 Automatic post reviewing
* 🔄 Automatic regeneration when the reviewer rejects a post
* 👤 Human approval before publishing
* 🔌 MCP client-server architecture
* 🛠️ Custom MCP tool for LinkedIn publishing
* 🔐 LinkedIn OAuth 2.0 authentication
* 🚀 Real LinkedIn API integration
* ✅ Publishes the complete generated post directly to LinkedIn

---

# 🏗️ Architecture

```text
                    ┌──────────────────────┐
                    │       User           │
                    │      enters topic    │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │      main.py         │
                    │  Application Entry   │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │     AI Writer        │
                    │  Gemini/ GROQ / LLM  │
                    └──────────┬───────────┘
                               │
                         Web Research
                               │
                               ▼
                    ┌──────────────────────┐
                    │   Tavily Search      │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   Generated Draft    │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │      Reviewer        │
                    │  Gemini/ GROQ / LLM  │
                    └──────────┬───────────┘
                               │
                  ┌────────────┴────────────┐
                  │                         │
              REJECTED                   APPROVED
                  │                         │
                  ▼                         ▼
              AI Writer              Human Approval
                  │                         │
                  └─────── Retry ───────────┤
                                            │
                                           Yes
                                            │
                                            ▼
                                  ┌──────────────────┐
                                  │    MCP Client    │
                                  └────────┬─────────┘
                                           │
                                           ▼
                                  ┌──────────────────┐
                                  │    MCP Server    │
                                  │                  │
                                  │ create_linkedin_ │
                                  │      post        │
                                  └────────┬─────────┘
                                           │
                                           ▼
                                  ┌──────────────────┐
                                  │   LinkedIn API   │
                                  └────────┬─────────┘
                                           │
                                           ▼
                                  ┌──────────────────┐
                                  │ Actual LinkedIn  │
                                  │      Post 🚀     │
                                  └──────────────────┘
```

---

# 🔄 Complete Workflow

### 1. User provides a topic

Example:

```text
What is Model Context Protocol and how does it help AI applications connect with external tools?
```

### 2. AI Writer generates the post

The writer uses an LLM to create a LinkedIn-friendly post.

If current information is required, the writer can use the Tavily web search tool.

---

### 3. Reviewer evaluates the post

The generated post is sent to a separate reviewer.

The reviewer checks things such as:

* Content quality
* Structure
* Relevance
* LinkedIn formatting
* Clarity
* Length
* Whether the post follows the writing requirements

The reviewer returns:

```text
APPROVED
```

or rejects the post with feedback.

---

### 4. Automatic regeneration

If the reviewer rejects the post:

```text
Writer
   ↓
Reviewer
   ↓
Rejected
   ↓
Feedback
   ↓
Writer
```

The writer uses the feedback to generate an improved version.

The project allows multiple attempts before stopping.

---

### 5. Human approval

After the reviewer approves the post, the application displays the complete post:

```text
Do you want to publish this post? (y/n):
```

The post is only sent to LinkedIn when the user enters:

```text
y
```

---

# 🔌 MCP Integration

The most important part of this project is the MCP integration.

The project contains an MCP client and MCP server.

```text
mcp_client/
└── client.py

mcp_server/
└── server.py
```

The client connects to the MCP server and discovers the available tools.

Currently, the server exposes:

```text
create_linkedin_post
```

The client calls the tool with:

```python
{
    "content": generated_post
}
```

The MCP server then handles the LinkedIn API request.

---

# 🧩 Why MCP?

Without MCP, the AI application could directly contain LinkedIn API integration:

```text
AI Application
      ↓
LinkedIn API
```

With MCP:

```text
AI Application
      ↓
   MCP Client
      ↓
   MCP Server
      ↓
 LinkedIn API
```

This separates the **AI application** from the **external service integration**.

The MCP server is responsible for exposing the capability as a tool:

```text
create_linkedin_post
```

This makes the external capability available through a standardized tool interface.

---

# 🔐 LinkedIn Authentication

The project uses LinkedIn OAuth 2.0 for authentication.

The authentication flow is:

```text
User
 ↓
/login
 ↓
LinkedIn Authorization
 ↓
Authorization Code
 ↓
/callback
 ↓
Access Token
 ↓
LinkedIn API
```

The application uses the LinkedIn permission:

```text
w_member_social
```

to publish posts on behalf of the authenticated LinkedIn member.

Sensitive credentials are stored in environment variables.

---

# 📁 Project Structure

```text
MCP_Learning/
│
├── main.py
│
├── linkedin_auth.py
│
├── agent/
│   ├── graph.py
│   ├── state.py
│   ├── prompt.py
│   └── tools.py
│
├── mcp_client/
│   └── client.py
│
├── mcp_server/
│   └── server.py
│
├── .env
├── .gitignore
└── README.md
```

### `main.py`

Main application entry point.

It:

* Takes the topic
* Runs the LangGraph workflow
* Displays the generated post
* Requests human approval
* Sends the approved post to the MCP client

---

### `agent/graph.py`

Contains the LangGraph workflow.

Responsible for:

* Writer
* Tool execution
* Draft extraction
* Reviewer
* Retry logic
* Approval routing

---

### `agent/prompt.py`

Contains the system prompts for:

* Writer
* Reviewer

---

### `agent/tools.py`

Contains tools available to the AI writer, including web search.

---

### `agent/state.py`

Defines the state shared between LangGraph nodes.

---

### `mcp_client/client.py`

Connects the AI application to the MCP server.

It:

1. Starts the MCP server
2. Discovers available tools
3. Calls `create_linkedin_post`
4. Returns the MCP result

---

### `mcp_server/server.py`

The MCP server.

It exposes:

```text
create_linkedin_post
```

and handles:

* Content validation
* LinkedIn authentication
* LinkedIn API request
* Publishing the post
* Returning the LinkedIn post ID

---

### `linkedin_auth.py`

Handles LinkedIn OAuth authentication and retrieves the access token and member information.

---

# 🛠️ Tech Stack

| Technology        | Purpose                   |
| ----------------- | ------------------------- |
| Python            | Main programming language |
| LangGraph         | AI workflow orchestration |
| LangChain         | LLM/tool integration      |
| Google Gemini     | Writer and reviewer       |
| Tavily            | Web research              |
| MCP               | AI-to-tool communication  |
| FastAPI           | LinkedIn OAuth server     |
| LinkedIn REST API | Publishing posts          |
| OAuth 2.0         | Authentication            |
| python-dotenv     | Environment variables     |

---

# ⚙️ Setup

## 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd MCP_Learning
```

---

## 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
venv\Scripts\activate
```

---

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure environment variables

Create a `.env` file:

```env
GOOGLE_API_KEY=your_google_api_key
TAVILY_API_KEY=your_tavily_api_key

LINKEDIN_CLIENT_ID=your_linkedin_client_id
LINKEDIN_CLIENT_SECRET=your_linkedin_client_secret
LINKEDIN_REDIRECT_URI=http://localhost:8000/callback

LINKEDIN_ACCESS_TOKEN=your_access_token
LINKEDIN_MEMBER_ID=your_member_id
```

**Never commit your `.env` file to GitHub.**

Add:

```text
.env
```

to `.gitignore`.

---

# ▶️ Running the Project

First, start the LinkedIn OAuth application if required:

```bash
uvicorn linkedin_auth:app --reload --port 8000
```

Then run the main application:

```bash
python main.py
```

Enter a topic:

```text
Topic: What is Model Context Protocol?
```

The application will:

```text
Generate
   ↓
Review
   ↓
Approve
   ↓
Ask user
   ↓
Publish through MCP
```

When prompted:

```text
Do you want to publish this post? (y/n):
```

Enter:

```text
y
```

The post will be published to LinkedIn through the MCP server.

---

# 🧪 Testing MCP Separately

You can also test the MCP client independently:

```bash
python mcp_client/client.py
```

Expected output:

```text
Connected to MCP server!

Available tools:
-create_linkedin_post

Tool result:
LinkedIn post published successfully!
Post ID: ...
```

---

# 🔒 Security

Never commit these values:

```text
LINKEDIN_CLIENT_SECRET
LINKEDIN_ACCESS_TOKEN
GOOGLE_API_KEY
TAVILY_API_KEY
```

Use environment variables instead.

The `.env` file should remain local.

---

# 📚 What I Learned

Through this project, I learned how to:

* Build an AI workflow using LangGraph
* Connect LLMs with external tools
* Use web search inside an AI workflow
* Implement reviewer-based generation
* Implement retry and feedback loops
* Implement human approval
* Understand MCP client-server architecture
* Create an MCP tool
* Connect an MCP server to a real external API
* Implement LinkedIn OAuth
* Use the LinkedIn REST API
* Build an end-to-end AI application using MCP

---

# 🚀 Future Improvements

Possible improvements include:

* [ ] Schedule LinkedIn posts
* [ ] Support multiple LinkedIn accounts
* [ ] Add image generation
* [ ] Add post analytics
* [ ] Add LinkedIn post history
* [ ] Add a web UI
* [ ] Add more MCP tools
* [ ] Add persistent token management
* [ ] Add better error handling and logging
* [ ] Deploy the MCP server

---

# 🎯 Project Goal

The main goal of this project is to understand **how MCP can be used to connect AI applications with real-world external tools and services**.

Instead of building an AI application that only generates text, this project demonstrates an AI system that can:

```text
Understand a task
      ↓
Research
      ↓
Generate
      ↓
Review
      ↓
Ask for approval
      ↓
Use an external tool
      ↓
Perform a real-world action
```

---

## ⭐ Project Highlight

> **This README describes a working MCP-based LinkedIn Post Generator where the AI-generated post is actually published to LinkedIn through an MCP client, MCP server, and LinkedIn API.**

---

## 👨‍💻 Author

**Harsh Adhana**

B.Tech CSE | AI & Machine Learning Enthusiast

Interested in:

* Artificial Intelligence
* Machine Learning
* Generative AI
* LLMs
* RAG
* AI Agents
* Model Context Protocol (MCP)

---

## ⭐ If you found this project useful

Feel free to explore the repository and connect with me on LinkedIn.
