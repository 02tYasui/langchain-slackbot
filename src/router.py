from fastapi import FastAPI
from langserve import add_routes
from fastapi.middleware.cors import CORSMiddleware

import ai_engine

from langsmith import Client

client = Client()
app = FastAPI(
    title="LangChain Server",
    version="1.0",
    description="A simple api server using Langchain's Runnable interfaces",
)

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello, World!"}


add_routes(
    app,
    ai_engine.chat_with_history(),
    path="/slack",
)
