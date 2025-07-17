# Agents leverage the reasoning capabilities of LLMs
# to make decisions during execution. 
from langchain_core.messages import AIMessage, HumanMessage
from langchain.tools.retriever import create_retriever_tool
from langgraph.prebuilt import create_react_agent
from pc_vector_store.retriever import retriever
from llms.chatgpt import llm
from persistence.memory import memory

config = {"configurable": {"thread_id": "abc123"}}

tool = create_retriever_tool(
    retriever,
    "wooster_college_retriever",
    "Searches and returns information from the College of Wooster Website.",
)

tools = [tool]
agent_executor = create_react_agent(llm, tools, checkpointer=memory)

query = "What is Dr.Visa's Research?"

for event in agent_executor.stream(
    {"messages": [HumanMessage(content=query)]},
    stream_mode="values",
    config=config
):
    event["messages"][-1].pretty_print()