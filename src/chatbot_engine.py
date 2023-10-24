from langchain.chat_models import ChatOpenAI
import langchain
from langchain.memory import ChatMessageHistory
from langchain.schema import HumanMessage
from langchain.document_loaders import DirectoryLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain.agents.agent_toolkits import (
    create_vectorstore_agent,
    VectorStoreToolkit,
    VectorStoreInfo
)
from typing import List
from langchain.tools import BaseTool
from langchain.memory import ConversationBufferMemory
from langchain.agents import initialize_agent, AgentType

langchain.verbose = True

def create_index() -> VectorStoreIndexWrapper:
    loader = DirectoryLoader("./src/", glob="**/*.py")
    return VectorstoreIndexCreator().from_loaders([loader])

def create_tools(index: VectorStoreIndexWrapper) -> List[BaseTool]:
    vectorstore_info =  VectorStoreInfo(
        name="udemy-langchain source code",
        description="Source code of application named udemy-langchain",
        vectorstore=index.vectorstore,
    )
    toolkit = VectorStoreToolkit(vectorstore_info=vectorstore_info)
    return toolkit.get_tools()

def chat(message: str, history: ChatMessageHistory, index: VectorStoreIndexWrapper) -> str:
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

    tools = create_tools(index)

    memory = ConversationBufferMemory(chat_memory = history, memory_key="chat_history", return_messages=True)

    agent_chain = initialize_agent(
        tools,
        llm,
        agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
        memory=memory
    )

    return agent_chain.run(input=message)