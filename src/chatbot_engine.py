import langchain
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain.schema import HumanMessage
from langchain_community.document_loaders import DirectoryLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain.agents.agent_toolkits import (
    create_vectorstore_agent,
    VectorStoreToolkit,
    VectorStoreInfo,
)
from langchain_openai import ChatOpenAI
from typing import List
from langchain.tools import BaseTool
from langchain.memory import ConversationBufferMemory
from langchain.agents import initialize_agent, AgentType
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter


langchain.verbose = True

# 定数の定義
MODEL_NAME = "gpt-3.5-turbo"
TEMPERATURE = 0


def create_index() -> VectorStoreIndexWrapper:
    """
    ソースコードディレクトリからベクターストアインデックスを作成します。
    """
    try:
        loader = DirectoryLoader("./src/", glob="**/*.py")
        documents = loader.load()
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        texts = text_splitter.split_documents(documents)

        embeddings = OpenAIEmbeddings()
        vectorstore = Chroma.from_documents(texts, embeddings)
        return VectorStoreIndexWrapper(vectorstore=vectorstore)

    except Exception as e:
        print(f"インデックス作成中にエラーが発生しました: {e}")
        raise


def create_tools(index: VectorStoreIndexWrapper) -> List[BaseTool]:
    llm = ChatOpenAI(model_name=MODEL_NAME, temperature=TEMPERATURE)

    vectorstore_info = VectorStoreInfo(
        name="langchain_source_code",
        description="Source code of application named udemy-langchain",
        vectorstore=index.vectorstore,
    )

    toolkit = VectorStoreToolkit(vectorstore_info=vectorstore_info, llm=llm)

    return toolkit.get_tools()


def chat(
    message: str,
    history: ChatMessageHistory,
    index: VectorStoreIndexWrapper,
) -> str:
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

    tools = create_tools(index)

    memory = ConversationBufferMemory(
        chat_memory=history, memory_key="chat_history", return_messages=True
    )

    agent_chain = initialize_agent(
        tools, llm, agent=AgentType.OPENAI_FUNCTIONS, memory=memory
    )

    return agent_chain.run(input=message)
