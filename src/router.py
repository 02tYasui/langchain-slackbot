from fastapi import FastAPI
from langserve import add_routes
from langchain.llms.fake import FakeListLLM


app = FastAPI(
    title="LangChain Server",
    version="1.0",
    description="A simple api server using Langchain's Runnable interfaces",
)


@app.get("/")
async def root():
    return {"message": "Hello, World!"}


# Add more routes here
responses = [
    "あのイーハトーヴォのすきとおった風",
    "夏でも底に冷たさをもつ青いそら",
    "うつくしい森で飾られたモリーオ市" "郊外のぎらぎらひかる草の波",
]

llm = FakeListLLM(responses=responses)

add_routes(
    app,
    FakeListLLM(responses=responses),
    path="/joke",
)
