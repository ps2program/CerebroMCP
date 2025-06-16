# Project: Full MCP + LangGraph + CrewAI App (Hybrid LLMs + Conditional Routing + SQLite Memory + RAG + Agents)

# Structure:
# ├── app/
# │   ├── main.py              <- Host application using LangGraph
# │   ├── clients/
# │   │   ├── openai_client.py
# │   │   ├── llama_client.py
# │   │   ├── rag_client.py
# │   │   └── crewai_client.py  <- New CrewAI client
# │   ├── servers/
# │   │   ├── llama_server.py
# │   │   ├── rag_mcp_server.py
# │   │   └── crewai_server.py  <- New CrewAI MCP server
# │   ├── host_managed/
# │   │   └── internal_llm.py
# │   └── memory/
# │       └── sqlite_memory.py
# ├── .env
# ├── requirements.txt

# -------------------- requirements.txt --------------------
mcp
openai
python-dotenv
langgraph
aiosqlite
langchain
chromadb
crewai

# -------------------- app/clients/crewai_client.py --------------------
from mcp import ClientSession
from mcp.client.stdio import StdioServerParameters

async def create_crewai_client():
    return await ClientSession.create(
        server=StdioServerParameters(command=["python", "app/servers/crewai_server.py"]),
        name="crewai-client"
    )

# -------------------- app/servers/crewai_server.py --------------------
from crewai import Agent, Task, Crew
from mcp.server.stdio import stdio_server

@stdio_server()
async def crewai_handler(prompt: str) -> str:
    researcher = Agent(name="Researcher", goal="Find useful knowledge", backstory="A domain expert")
    writer = Agent(name="Writer", goal="Summarize well", backstory="Tech writer")

    task = Task(description=prompt, expected_output="Insightful and clear response", agent=researcher)

    crew = Crew(agents=[researcher, writer], tasks=[task], process="sequential")
    result = crew.kickoff()
    return result

# -------------------- app/main.py --------------------
import asyncio
from langgraph.graph import StateGraph
from langgraph.graph.graph import State
from app.clients.openai_client import create_openai_client
from app.clients.llama_client import create_llama_client
from app.clients.rag_client import create_rag_client
from app.clients.crewai_client import create_crewai_client
from app.host_managed.internal_llm import query_internal_llm
from app.memory.sqlite_memory import init_memory, load_memory, save_memory

class LLMState(State):
    input: str
    output: str = ""
    route: str = ""
    memory: str = ""

def should_use_internal(prompt: str) -> bool:
    return len(prompt.split()) < 5

def should_use_openai(prompt: str) -> bool:
    return "explain" in prompt.lower()

def should_use_rag(prompt: str) -> bool:
    return any(word in prompt.lower() for word in ["document", "retrieve", "design", "paper"])

def should_use_crewai(prompt: str) -> bool:
    return "analyze" in prompt.lower() or "research" in prompt.lower()

async def internal_node(state: LLMState) -> LLMState:
    output = await query_internal_llm(state.input, state.memory)
    state.output = output
    state.memory += f"\nUser: {state.input}\nInternal: {output}"
    await save_memory(state.memory)
    return state

async def openai_node(state: LLMState, openai_client) -> LLMState:
    output = await openai_client.send(state.input)
    state.output = output
    state.memory += f"\nUser: {state.input}\nOpenAI: {output}"
    await save_memory(state.memory)
    return state

async def llama_node(state: LLMState, llama_client) -> LLMState:
    output = await llama_client.send(state.input)
    state.output = output
    state.memory += f"\nUser: {state.input}\nLLaMA: {output}"
    await save_memory(state.memory)
    return state

async def rag_node(state: LLMState, rag_client) -> LLMState:
    output = await rag_client.send(state.input)
    state.output = output
    state.memory += f"\nUser: {state.input}\nRAG: {output}"
    await save_memory(state.memory)
    return state

async def crewai_node(state: LLMState, crewai_client) -> LLMState:
    output = await crewai_client.send(state.input)
    state.output = output
    state.memory += f"\nUser: {state.input}\nCrewAI: {output}"
    await save_memory(state.memory)
    return state

async def main():
    await init_memory()
    memory = await load_memory()

    openai_client = await create_openai_client()
    llama_client = await create_llama_client()
    rag_client = await create_rag_client()
    crewai_client = await create_crewai_client()

    async def route_node(state: LLMState) -> str:
        if should_use_crewai(state.input):
            return "llm_crewai"
        elif should_use_rag(state.input):
            return "llm_rag"
        elif should_use_internal(state.input):
            return "llm_internal"
        elif should_use_openai(state.input):
            return "llm_openai"
        else:
            return "llm_llama"

    graph = StateGraph(LLMState)
    graph.add_node("llm_internal", internal_node)
    graph.add_node("llm_openai", lambda s: openai_node(s, openai_client))
    graph.add_node("llm_llama", lambda s: llama_node(s, llama_client))
    graph.add_node("llm_rag", lambda s: rag_node(s, rag_client))
    graph.add_node("llm_crewai", lambda s: crewai_node(s, crewai_client))

    graph.add_conditional_edges("route", route_node, {
        "llm_internal": "end",
        "llm_openai": "end",
        "llm_llama": "end",
        "llm_rag": "end",
        "llm_crewai": "end",
    })
    graph.set_entry_point("route")

    app = graph.compile()

    while True:
        prompt = input("\nEnter your prompt (or 'exit'): ")
        if prompt.lower() == "exit":
            break
        state = LLMState(input=prompt, memory=memory)
        result = await app.run(state)
        memory = result.memory
        print("\nFinal Output:", result.output)

    await openai_client.aclose()
    await llama_client.aclose()
    await rag_client.aclose()
    await crewai_client.aclose()

if __name__ == "__main__":
    asyncio.run(main())
