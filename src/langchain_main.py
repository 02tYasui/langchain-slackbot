import os
import boto3 #Lambdaで動作する際に必要
from langchain_openai import ChatOpenAI
from langchain_community.chat_message_histories import DynamoDBChatMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


def chat_with_history():
    """履歴保持チャット"""
    model = ChatOpenAI(model=os.environ.get("MODEL_NAME"), temperature=0)

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "あなたは親切で優秀なAIアシスタントです。"),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{user_input}"),
        ]
    )

    chain = prompt | model | StrOutputParser()

    runnable_agent = RunnableWithMessageHistory(
        runnable=chain,
        get_session_history=lambda session_id: DynamoDBChatMessageHistory(
            table_name=os.environ.get("DYNAMODB_TABLE_NAME"), session_id=session_id
        ),
        input_messages_key="user_input",
        history_messages_key="history",
    )

    return runnable_agent
