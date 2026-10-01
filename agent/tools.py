from langchain_tavily import TavilySearch
from dotenv import load_dotenv

load_dotenv()

# tools

search_tool = TavilySearch(max_results = 3)

tool = [search_tool]