import asyncio
from mcp.client.socket import socket_client, SocketServerParameters
from mcp import ClientSession

async def main():
    server_params = SocketServerParameters(host="127.0.0.1", port=8765)
    async with socket_client(server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            print("Connected to persistent MCP server at 127.0.0.1:8765")
            while True:
                prompt = input("Enter your prompt (or 'quit' to exit): ")
                if prompt.lower() == "quit":
                    break
                response = await session.call_tool("echo_handler", {"prompt": prompt})
                if response.content and hasattr(response.content[0], 'text'):
                    print("Response:", response.content[0].text)
                else:
                    print("No response or invalid response format.")

if __name__ == "__main__":
    asyncio.run(main()) 