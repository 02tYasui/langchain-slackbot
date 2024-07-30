import os
from langchain_openai import ChatOpenAI
from langchain_core.chat_history import (
    BaseChatMessageHistory,
    InMemoryChatMessageHistory,
)
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.document_loaders import TextLoader
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter
from langchain_chroma import Chroma
from langchain.tools.retriever import create_retriever_tool
from langchain.agents import (
    AgentExecutor,
    create_tool_calling_agent,
)

store = {}


def chat_with_history():
    """履歴保持チャット"""
    model = ChatOpenAI(model=os.environ.get("MODEL_NAME"), temperature=0)

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "あなたは親切で優秀なAIアシスタントです。"),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{user_input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )

    raw_documents = TextLoader("./vector_file/sample.txt").load()
    text_splitter = CharacterTextSplitter(
        chunk_size=100,
        chunk_overlap=0,
        separator="\\n",
    )
    documents = text_splitter.split_documents(raw_documents)
    vectorstore = Chroma.from_documents(documents, OpenAIEmbeddings())
    retriever = vectorstore.as_retriever(chain_type_kwargs={"prompt": prompt})

    tools = [
        create_retriever_tool(
            retriever=retriever,
            name="Syugyoukisoku",
            description="就業規則について回答する場合に使用します。",
        ),
    ]

    agent = create_tool_calling_agent(model, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools)

    runnable_agent = RunnableWithMessageHistory(
        runnable=agent_executor,
        get_session_history=_get_session_history,
        input_messages_key="user_input",
        history_messages_key="history",
    )

    return runnable_agent


def _get_session_history(session_id: str) -> BaseChatMessageHistory:
    """ローカルメモリにセッション履歴保存・取得"""
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]
