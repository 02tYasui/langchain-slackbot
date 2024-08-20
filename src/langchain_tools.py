from langchain_community.tools import DuckDuckGoSearchRun
from langchain_vector import vector_to_tool

all_tools = [DuckDuckGoSearchRun(), vector_to_tool()]
