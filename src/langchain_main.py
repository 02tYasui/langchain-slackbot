import os
from langchain_openai import ChatOpenAI
from langchain_core.chat_history import (
    BaseChatMessageHistory,
    InMemoryChatMessageHistory,
)
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import (
    AgentExecutor,
    create_tool_calling_agent,
)

from langchain_tools import all_tools

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

    agent = create_tool_calling_agent(model, all_tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=all_tools)

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
