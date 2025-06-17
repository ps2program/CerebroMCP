from mcp import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client
from contextlib import asynccontextmanager

@asynccontextmanager
async def create_openai_client():
    server_params = StdioServerParameters(command="python", args=["app/servers/openai_server.py"])
    async with stdio_client(server_params) as (read_stream, write_stream):
        session = ClientSession(read_stream, write_stream)
        try:
            yield session
        finally:
            await session.aclose() 